from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated  # Add this line

from authors.models import AppUser
from posts.models import Post
from posts.models import Comment

from .models import GitHubFeed
from .serializers import GitHubFeedSerializer
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(description="Get all GitHub feeds for a user", responses={200: GitHubFeedSerializer(many=True), 404: "Not found"})
class GitHubFeedList(generics.ListAPIView):
    serializer_class = GitHubFeedSerializer
    permission_classes = (IsAuthenticated,)  # Require authentication

    def get_queryset(self):
        username = self.request.user.username  # Get authenticated user's username

        if username:
            github_api_url = f'https://api.github.com/users/{username}/feeds'
            response = requests.get(github_api_url)
            if response.status_code == 200:
                feeds_data = response.json()
                feeds = feeds_data.get('items', [])
                return [GitHubFeed(title=feed.get('title'), description=feed.get('description')) for feed in feeds]

        return []
