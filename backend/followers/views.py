from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.models import AppUser
from authors.serializers import UserSerializer
from .models import FriendRequest
from .serializers import FriendRequestSerializer
from inbox.models import Inbox

class FollowerList(APIView):
    """List all the followers of a given user."""

    def get(self, request, user_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        serializer = UserSerializer(user.followers.all(), many=True)
        return Response({"type": "followers", "items": serializer.data}, status=status.HTTP_200_OK)


class AcceptFriendRequest(APIView):
    """Accept a friend request """

    def post(self, request, user_id, requester_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        requester = get_object_or_404(AppUser, pk=requester_id)

        friend_request = FriendRequest.objects.filter(actor=requester, object=user).first()
        if not friend_request:
            return Response({"detail": "Friend request does not exist."}, status=status.HTTP_404_NOT_FOUND)

        user.followers.add(requester)  # User follows the requester
        
        friend_request.accepted = True
        friend_request.save()


        # notification for the requester (sender) of the friend request
        notification_summary = f"{user.username} accepted your friend request."
        notification = FriendRequest.objects.create(
            actor=user,  #  the actor is now the acceptor
            object=requester,  # The original person that sent request
            summary=notification_summary,
            type="Notification",  # distinguish it from regular friend requests
        )
        requester_inbox, _ = Inbox.objects.get_or_create(authorId=requester)
        requester_inbox.follow_request.add(notification)
        return Response({"detail": "Friend request accepted. Following the requester."}, status=status.HTTP_200_OK)


class EstablishMutualFriendship(APIView):
    """Establish mutual friendship between two users."""

    def post(self, request, user_id, friend_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        friend = get_object_or_404(AppUser, pk=friend_id)
        friend_request = FriendRequest.objects.filter(actor=friend_id, object=user, accepted=True).first()

        # Check if user is already following the friend
        print('all user followers', user.followers)
        print('all user friend request', friend_request)
        if friend in user.followers.all():

            user.followers.add(friend)  # Establish mutual friendship
            friend_request.delete()
            print('user follwoers', user.followers.all())
            return Response({"detail": "Mutual friendship established."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Mutual friendship cannot be established."}, status=status.HTTP_400_BAD_REQUEST)

class FollowerDetail(APIView):
    """Handle follower details for a user."""

    def get(self, request, user_id, follower_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        follower = get_object_or_404(AppUser, pk=follower_id)
        is_following = follower in user.followers.all()

        if not is_following:
            return Response({"type": "follower", "detail": "User is not following."}, status=status.HTTP_200_OK)

        serializer = UserSerializer(follower)
        return Response({"type": "follower", "items": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, user_id, follower_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        follower = get_object_or_404(AppUser, pk=follower_id)
        user.followers.add(follower)
        return Response({"type": "follower", "detail": "Follower added."}, status=status.HTTP_200_OK)

    def delete(self, request, user_id, follower_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        follower = get_object_or_404(AppUser, pk=follower_id)
        user.followers.remove(follower)
        return Response({"type": "follower", "detail": "Follower removed."}, status=status.HTTP_200_OK)

class FriendRequestList(APIView):
    """List all friend requests of a given user."""

    def get(self, request, user_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        print('is user valid', user.username)
        print('does this even work', user.recieved_friend_request.all())
        serializer = FriendRequestSerializer(user.recieved_friend_request.all(), many=True)
        print(serializer.data)
        return Response({"type": "friendRequestsRecieved", "items": serializer.data}, status=status.HTTP_200_OK)


class SentFriendRequestList(APIView):
    """List all friend requests sent by a given user."""

    def get(self, request, user_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        sent_requests = FriendRequest.objects.filter(actor=user)
        serializer = FriendRequestSerializer(sent_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FriendRequestDetail(APIView):
    """Handle friend request details for a user."""

    def get(self, request, user_id, requester_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        requester = get_object_or_404(AppUser, pk=requester_id)
        friend_request = FriendRequest.objects.filter(actor=requester, object=user).first()

        if not friend_request:
            return Response({"type": "friendRequest", "detail": "No pending friend request."}, status=status.HTTP_200_OK)

        serializer = FriendRequestSerializer(friend_request)
        return Response({"type": "friendRequest", "items": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, user_id, requester_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        requester = get_object_or_404(AppUser, pk=requester_id)
        friend_request, created = FriendRequest.objects.get_or_create(actor=requester, object=user)
        
        if created:
            return Response({"type": "friendRequest", "detail": "Friend request sent."}, status=status.HTTP_200_OK)
        else:
            return Response({"type": "friendRequest", "detail": "Friend request already exists."}, status=status.HTTP_200_OK)

    def delete(self, request, user_id, requester_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        requester = get_object_or_404(AppUser, pk=requester_id)
        FriendRequest.objects.filter(actor=requester, object=user).delete()
        return Response({"type": "friendRequest", "detail": "Friend request deleted."}, status=status.HTTP_200_OK)
