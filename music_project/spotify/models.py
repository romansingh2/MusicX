from django.db import models
from api.models import Room

class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)


class Vote(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    song_id = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #when we have a foreign key, we are passing an instance of another object, in this case a room object to the vote model. Any room we have stored in our database, we can pass one of those when we create a new vote. This way when we have a vote we can determine what room it was in
    #on delete means what should we do if the room is deleted
    #models.cascade means cascade down and delete anything that was referencing this room, ie if a room is deleted, all votes for that room are deleted
