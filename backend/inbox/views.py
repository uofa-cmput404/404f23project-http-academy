from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.models import AppUser
from posts.models import Post
from followers.models import FriendRequest
from followers.serializers import FriendRequestSerializer
from posts.serializers import PostSerializer
from like.serializers import LikeSerializer
from .models import Inbox
from like.models import Like

class InboxView(APIView):
    """
    API view to manage the inbox of an AppUser.
    """

    def get(self, request, author_id, format=None):
        """
        Retrieves all posts and likes from the inbox of the specified AppUser.
        """
        author = get_object_or_404(AppUser, pk=author_id)
        inbox = get_object_or_404(Inbox, authorId=author)

        # Serialize posts and likes
        posts_serializer = PostSerializer(inbox.posts.all().order_by("-published"), many=True)
        likes_serializer = LikeSerializer(inbox.like.all(), many=True)
        follow_serializer = FriendRequestSerializer(inbox.follow_request.all(), many = True)
        response = {
            "type": "inbox",
            "author_id": author.user_id,
            "posts": posts_serializer.data,
            "likes": likes_serializer.data,
            "follow_request": follow_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, author_id, format=None):
        """
        Adds a post or like to the inbox of the specified AppUser.
        """
        # print('i actually got hete')
        author = get_object_or_404(AppUser, pk=author_id)
        inbox, _ = Inbox.objects.get_or_create(authorId=author)
        # print('data i sent', request.data)
        request_type = request.data.get("type", "").lower()
        if request_type == "post":
            return self._add_post_to_inbox(request.data, inbox)
        elif request_type == "like":
            return self._add_like_to_inbox(request.data, inbox)
        elif request_type == "follow":
            return self._add_follow_request_to_inbox(request.data, inbox)
        
        return Response({"detail": "Unsupported request type"}, status=status.HTTP_400_BAD_REQUEST)

    def _add_post_to_inbox(self, post_data, inbox):
        post_id = post_data.pop('id', None)
        post_data.pop('author', None)
        post_data.pop('comments', None)

        # Assuming authorId in Inbox is the post author
        post_author = inbox.authorId

        # Check if a post with this ID already exists
        existing_post = Post.objects.filter(id=post_id).first()
        if existing_post:
            # If the post already exists, update it
            for key, value in post_data.items():
                setattr(existing_post, key, value)
            existing_post.save()
            # Add the existing post to the inbox
            inbox.posts.add(existing_post)
        else:
            # If the post does not exist, create a new one
            new_post = Post.objects.create(id=post_id, **post_data, author=post_author)
            inbox.posts.add(new_post)

        return Response({"detail": "Post processed for inbox"}, status=status.HTTP_201_CREATED)

    def _add_like_to_inbox(self, like_data, inbox):
        """
        Adds a like to the specified AppUser's inbox.
        """
        like = Like.objects.create(**like_data, author=inbox.authorId)
        inbox.like.add(like)
        return Response({"detail": "Like added to inbox"}, status=status.HTTP_201_CREATED)

    def _extract_uuid_from_url(self, url):
        # Split the URL and get the last non-empty segment
        parts = url.rstrip('/').split('/')
        return parts[-1]

    def _add_follow_request_to_inbox(self, follow_data, inbox):
        print('heree', follow_data)
        print('heree inbox', inbox)

        actor_data = follow_data.get('actor', {})
        object_data = follow_data.get('object', {})

        # Extract UUIDs from URLs
        actor_id = self._extract_uuid_from_url(actor_data.get('id'))
        object_id = self._extract_uuid_from_url(object_data.get('id'))

        print('actor_id,', actor_id)
        print('object_id,', object_id)

        summary = follow_data.get('summary')

        # Use UUIDs to fetch AppUser objects
        actor = get_object_or_404(AppUser, pk=actor_id)
        object = get_object_or_404(AppUser, pk=object_id)

        follow_request = FriendRequest.objects.create(actor=actor, object=object, summary=summary)
        inbox.follow_request.add(follow_request)
        print("Follow request added to inbox", inbox)
        return Response({"detail": "Follow request added to inbox"}, status=status.HTTP_201_CREATED)

    def delete(self, request, author_id, format=None):
        """
        Clears the inbox of the specified AppUser.
        """
        author = get_object_or_404(AppUser, pk=author_id)
        inbox = get_object_or_404(Inbox, authorId=author)

        inbox.posts.clear()
        inbox.like.clear()
        return Response({"detail": f"Inbox of {author.username} cleared successfully"}, status=status.HTTP_204_NO_CONTENT)




