#serializer will take model that has lots of python code and translate it into a json response
#JSON is a lightweight format for storing and transporting data
#JSON is often used when data is sent from a server to a web page

from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room #use the room model for this serializer
        fields = ('id', 'code', 'host', 'guest_can_pause', 'votes_to_skip', 'created_at') #list all the fields we want to include in the output/serialization
        #id is the primary key used to identify each row on the model, automatically created when we make a model

class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')

class UpdateRoomSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[]) #redefined code field right in serializer, this is because we set it up that code must be unique, but if we are just updating a room we want the code to not change, so we will not reference code field from model

    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip', 'code')

