from django.db import models
import string
import random 

def generate_unique_code():
    length = 6

    while True:  
        code = ''.join(random.choices(string.ascii_uppercase, k=length)) #create random assortment of uppercase characters room ascii tables with k length
        if Room.objects.filter(code=code).count() == 0: #if the code does not exist in the room table, break the function and return the code, otherwise keep repeating until the code is unique
            break
        
    return code

# Create your models here.

class Room(models.Model):
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True) #unique identifier code, max length is 8 and the code must be unique each time, ie no hosts can share the same code
    host = models.CharField(max_length=50, unique=True) #the person hosting the room, max length is 50 and username of host must be unique
    guest_can_pause = models.BooleanField(null=False, default=False) #can the guest pause the music? either true or false, default false
    votes_to_skip = models.IntegerField(null=False, default=1) #number of votes required to skip the song
    created_at = models.DateTimeField(auto_now_add=True) #when we create a room it will automatically include date and time room was created
    current_song = models.CharField(max_length=50, null=True)
