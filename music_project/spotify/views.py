from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import *
from api.models import Room
from .models import Vote

#1. Have your application request authorization; the user logs in and authorizes access 
class AuthURL(APIView): #this is an api endpoint that will return to us a url
    def get(self, request, format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'         #a scope is what information you want to have access to

        url = Request('GET', 'https://accounts.spotify.com/authorize', params = {
            'scope':  scopes,
            'response_type': 'code', #we are requesting we get sent a code back that will allow us to authenticate a user
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url       #return a url where we can go to to authenticate our spotify application
                                #after we send the request to the url, we need a callback or some url where this information returns to
        return Response({'url': url}, status=status.HTTP_200_OK)

#after we send the request to the url in the get function, we return the information to this function
#inside this function we then send a request using the code to get access to the access token and other info



def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)


    return redirect('frontend:')

class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)

class CurrentSong(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
        else: 
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        host = room.host
        endpoint = "player/currently-playing" 
        response = execute_spotify_api_request(host, endpoint)
        
        if 'error' in response or 'item' not in response: #if there is an error or no song is currently on
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        item = response.get('item')
        duration = item.get('duration_ms')
        progress = item.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url')
        is_playing = response.get('is_playing')
        song_id = item.get('id')

        artist_string = ""

        for i, artist in enumerate(item.get('artists')): #might be multiple artists, The enumerate() method adds counter to an iterable and returns it (the enumerate object).
            if i > 0:  #if i is not the first artist in the list
                artist_string += ", "
            name = artist.get('name') #name of the artist
            artist_string += name #append the name to the list of artists for a song
        
        votes = len(Vote.objects.filter(room=room, song_id=song_id))   
        song = {
            'title': item.get('name'),
            'artist': artist_string,
            'duration': duration,
            'time': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            'votes': votes,
            'votes_required': room.votes_to_skip,
            'id': song_id
        }

        self.update_room_song(room, song_id)

        return Response(song, status=status.HTTP_200_OK)
    
    def update_room_song(self, room, song_id):
        current_song = room.current_song

        if current_song != song_id: #if these are not equal, it means song changed
            room.current_song = song_id
            room.save(update_fields=['current_song']) #when a song is changed we need to get rid of votes associated with the previous song
            votes = Vote.objects.filter(room=room).delete()


class PauseSong(APIView):
    def put(self, response, format=None):
            #first thing we need to make sure is if user sending this request actually has permission to pause or play the song
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        #check whether guests are allowed to play or pause song, or if current user is host
        if self.request.session.session_key == room.host or room.guest_can_pause:
            pause_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({}, status=status.HTTP_403_FORBIDDEN)

class PlaySong(APIView):
    def put(self, response, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            play_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({}, status=status.HTTP_403_FORBIDDEN)

class SkipSong(APIView):
    def post(self, request, format=None):
        room_code = self.request.session.get('room_code') #access the host access token so we can send the request to spotify
        room = Room.objects.filter(code=room_code)[0]
        votes = Vote.objects.filter(room=room, song_id=room.current_song) #get the current votes
        votes_needed = room.votes_to_skip #votes needed to skip

        if self.request.session.session_key == room.host or len(votes) + 1 >= votes_needed: #if the host is the one sending the request
            votes.delete() #delete the votes for the current song right before skipping
            skip_song(room.host) #use the host as the session id/key
        else: 
            vote = Vote(user=self.request.session.session_key, 
                        room=room, song_id=room.current_song)
            vote.save() #create a new vote in the database

        return Response({}, status.HTTP_204_NO_CONTENT)

