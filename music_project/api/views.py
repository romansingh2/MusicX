from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room
from rest_framework.views import APIView   
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.
#this is where we write all of our endpoints

class RoomView(generics.ListAPIView):  # a class is a blueprint for an object
    queryset = Room.objects.all() # return all the objects in the room model
    serializer_class = RoomSerializer #convert this into some format that i can actually return, ie convert it into json. Use the room serializer in serializers.py
     
class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code' #when we call the GetRoom apiview with the get request, we need to pass a parameter in the url called code and that code will be equal to the room we are trying to get

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg) #retrieve the code from the url
        if code != None: #if code is not equal to none
            room = Room.objects.filter(code=code) #filter out the room objects that have the code, since code is unique we should only get one value
            if len(room) > 0: #if we do have a room
                data = RoomSerializer(room[0]).data #we are serializing the room object, and taking the data which is a python dictionary and extracting it from the room serializer. 
                data['is_host'] = self.request.session.session_key == room[0].host #the host will be the session key of whoever is the host of the room. We can check our current session key and see if it is equal to room[0].host, and if it is that means the user is the host. if not, that means they are not the host. 
                return Response(data, status=status.HTTP_200_OK) #return the data and status 200
            return Response({'Room Not Found': 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND) #if there is no room return this response
        #if no code was entered
        return Response({'Bad Request': 'Code parameter not found  in request'}, status = status.HTTP_400_BAD_REQUEST)

class JoinRoom(APIView):
    lookup_url_kwarg = 'code'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key): #check if current user has active session with our web server. A session is a temporary connection between two devices
            self.request.session.create() #if they do not have a session, create one

        code = request.data.get(self.lookup_url_kwarg)  #with post requests we can use just .data field, with get we need .get
        if code != None:  #if the code was not equal to none
            room_result = Room.objects.filter(code=code) #set room_result equal to the room(s) with the code
            if len(room_result) > 0: #if room(s) were found
                room = room_result[0]
                self.request.session['room_code'] = code #this user in its current session is in this room. self.request.session stores information in a variable called room_code, which is equal to the code
                return Response({'message': 'Room Joined!'}, status=status.HTTP_200_OK)
            return Response({'Bad Request': 'Invalid Room Code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response ({'Bad Request': 'Invalid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)


class CreateRoomView(APIView): #APIView lets us override some default methods
    serializer_class = CreateRoomSerializer #set the variable serializer_class equal to the CreateRoomSerializer we made in serializers.py 
    
    def post(self, request, format=None):
        #self represents the instance of the class. By using the “self” keyword we can access the attributes and methods of the class in python. It binds the attributes with the given arguments.
        #self can be replaced with any other word, but is used for readability
        
        if not self.request.session.exists(self.request.session.session_key): #check if current user has active session with our web server. A session is a temporary connection between two devices
            self.request.session.create() #if they do not have a session, create one
        
        serializer = self.serializer_class(data=request.data) #take all of our data, serialize it, and give us some python representation of it. 
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause') #set the variable guest_can_pause equal to the value of the variable of the same name in models
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key #session key is used to identify the host

            #need to check if the person trying to create a room already has an active room, if they do, rather than creating a new room we will just update the settings of the current active room, but same room code
            queryset = Room.objects.filter(host=host) #look in the database to see if any rooms have the same host that is trying to create a room, in other words, check if the host trying to create a room already has an active one
            if queryset.exists(): #if we are updating a room
                room = queryset[0]
                room.guest_can_pause = guest_can_pause #update the value of guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip']) #update the fields
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK) 
            else: #if we are not updating a room we are creating one
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
                self.request.session['room_code'] = room.code

            
            #we want to return a response to tell the user whether their response 
            # was valid or not, this response will contain the room they created with 
            # extra information like the id and the time it was created at, do that we need 
            # to serialize the room object we just created
            
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)



class UserInRoom(APIView): #are they in a room? if they are return a roomcode 
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key): #check if current user has active session with our web server. A session is a temporary connection between two devices
            self.request.session.create() #if they do not have a session, create one
            
        data = {
            'code': self.request.session.get('room_code')
        }

        return JsonResponse(data, status=status.HTTP_200_OK) #take a python dictionary and serialize it using a json serializer and then sends that information back 


class LeaveRoom(APIView):
    def post(self, request, format=None):
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code') #remove room code from the user session
            host_id = self.request.session.session_key #checking if they are hosting a room
            room_results = Room.objects.filter(host=host_id) #check if the user is the host
            if len(room_results) > 0: #if the host is the one leaving the room
                room = room_results[0]
                room.delete() #if the host leaves, delete the room

        return Response({'Message': 'Success'}, status=status.HTTP_200_OK)

class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key): #check if current user has active session with our web server. A session is a temporary connection between two devices
            self.request.session.create()
        #use patch whenever you are updating something 
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = serializer.data.get('code')

            queryset = Room.objects.filter(code=code)
            if not queryset.exists(): #if no room found we cannot update room because it does not exist
                return Response({'msg': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)
            #if we do find a room
            room = queryset[0]
            #make sure person who is trying to update room is the one who created it, we need to get their session key and check it against the host of the room
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response({'msg': 'You are not the host of this room.'}, status=status.HTTP_403_FORBIDDEN)
            room.guest_can_pause = guest_can_pause 
            room.votes_to_skip = votes_to_skip 
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)


        return Response({"Bad Request": "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST)

         