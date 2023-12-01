
from importlib.metadata import requires
from rest_framework import serializers

from authors.serializers import UserSerializer
from .models import GitHubFeed


class GitHubFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubFeed
        fields = ('title', 'description')
