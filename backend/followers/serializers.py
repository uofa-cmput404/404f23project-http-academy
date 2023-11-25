
from rest_framework import serializers
from .models import FriendRequest
from authors.serializers import UserSerializer


class FriendRequestSerializer(serializers.ModelSerializer):
   
    actor = UserSerializer(many=False, required=True)
    object = UserSerializer(many=False, required=True)
    summary = serializers.CharField(max_length=100, required=False)
    accepted = serializers.BooleanField(read_only = True)
    class Meta:
        model = FriendRequest
        fields = ("type", "summary", "actor", "object", "accepted")
