
from importlib.metadata import requires
from rest_framework import serializers

from authors.serializers import UserSerializer
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="Like", read_only=True)
    author = UserSerializer(many=False, required=True)

    class Meta:
        model = Like
        fields = ['type', 'author', 'object', 'summary']


