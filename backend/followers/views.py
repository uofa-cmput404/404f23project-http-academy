from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.models import AppUser
from authors.serializers import UserSerializer
from .models import FriendRequest
from .serializers import FriendRequestSerializer
from inbox.models import Inbox
from drf_yasg.utils import swagger_auto_schema

class FollowerList(APIView):
    """List all the followers of a given user."""
    @swagger_auto_schema(
        operation_description="Retrieve all followers of the specified AppUser.",
        responses={200: UserSerializer(many=True), 404: "Not found"}
    )
    def get(self, request, user_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        serializer = UserSerializer(user.followers.all(), many=True)
        print('this view was activated', serializer.data)
        return Response({"type": "followers", "items": serializer.data}, status=status.HTTP_200_OK)


class UnfriendUser(APIView):
    @swagger_auto_schema(
        operation_description="Unfriend a user.",
        responses={200: "{'detail': 'Unfriended successfully'}"}
    )
    def delete(self, request, user_id, requester_id):
        user = get_object_or_404(AppUser, pk=user_id)
        other_user = get_object_or_404(AppUser, pk=requester_id)

        # Remove the other user from user's following and followers
        user.following.remove(other_user)
        user.followers.remove(other_user)

        # remove user from other user's following and followers
        other_user.following.remove(user)
        other_user.followers.remove(user)

        return Response({"detail": "Unfriended successfully"}, status=status.HTTP_200_OK)
    
class AcceptFriendRequest(APIView):
    """Accept a friend request."""
    @swagger_auto_schema(
        operation_description="Accept a friend request.",
        request_body=FriendRequestSerializer,
        responses={200: "{'type': 'friendRequest', 'detail': 'Friend request sent.'}", 404: "{'type': 'friendRequest', 'detail': 'Friend request does not exist or is already accepted.'}"}
    )
    def post(self, request, user_id, requester_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        requester = get_object_or_404(AppUser, pk=requester_id)

        print(' iaccepted ur request - THIS IS ME', user)
        print(' iaccepted ur request - THIS IS YOUU THE REQUESTER', requester)
        # Check if the friend request exists and is not already accepted
        friend_request = FriendRequest.objects.filter(actor=requester, object=user).first()
        if not friend_request or friend_request.accepted:
            return Response({"detail": "Friend request does not exist or is already accepted."}, status=status.HTTP_404_NOT_FOUND)

        # User follows the requester (user adds requester to its following list)
        #here iam addign the requester to my folowing list
        print('user 1', user)
        print('REQUESTER USER 2 ', requester)
        requester.following.add(user)
        user.followers.add(requester)

      
        friend_request.accepted = True
        friend_request.save()

        print(' at east i got here')
        # Create and send notification to the requester
        notification_summary = f"{user.username} accepted your friend request."
        notification, created = FriendRequest.objects.get_or_create(
            actor=user,  # the actor is now the acceptor
            object=requester,  # the original person that sent request
            summary=notification_summary,
            type="Notification",  # distinguish it from regular friend requests
        )
        requester_inbox, _ = Inbox.objects.get_or_create(authorId=requester)
        requester_inbox.follow_request.add(notification)
        
        if created:
            return Response({"type": "friendRequest", "detail": "Friend request sent."}, status=status.HTTP_200_OK)
        else:
            return Response({"type": "friendRequest", "detail": "Friend request already exists."}, status=status.HTTP_200_OK)

    def delete(self, request, user_id, requester_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        requester = get_object_or_404(AppUser, pk=requester_id)
        FriendRequest.objects.filter(actor=requester, object=user).delete()
        return Response({"type": "friendRequest", "detail": "Friend request deleted."}, status=status.HTTP_200_OK)


class FollowingList(APIView):
    """List all the users that a given user is following."""
    
    def get(self, request, user_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        following_users = user.following.all()
        serializer = UserSerializer(following_users, many=True)
        print('followin list', serializer.data)
        return Response({"type": "following", "items": serializer.data}, status=status.HTTP_200_OK)


class EstablishMutualFriendship(APIView):
    """Establish mutual friendship between two users."""

    def post(self, request, user_id, friend_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        friend = get_object_or_404(AppUser, pk=friend_id)
        friend_request = FriendRequest.objects.filter(actor=friend_id, object=user, accepted=True).first()

        # Check if user is already following the friend
        print('all user followers', user.followers.all())
        print('all user friend request', friend_request)
        if friend in user.followers.all():

            user.following.add(friend)  # Establish mutual friendship
            friend.followers.add(user) #establish mutual friendship
            friend_request.delete() #no need to kee pthe requets no more 
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

        # Check if there's an existing friend request
        friend_request = FriendRequest.objects.filter(actor=follower, object=user).first()
        if friend_request:
            friend_request.accepted = True
            friend_request.save()

            # Remove friend request from user's inbox
            user_inbox, _ = Inbox.objects.get_or_create(authorId=user)
            user_inbox.follow_request.remove(friend_request)

            # Send notification to requester's inbox
            notification_summary = f"{user.username} accepted your friend request."
            notification = FriendRequest.objects.create(
                actor=user,
                object=follower,
                summary=notification_summary,
                type="Notification",
            )
            follower_inbox, _ = Inbox.objects.get_or_create(authorId=follower)
            follower_inbox.follow_request.add(notification)

        # Add follower
        user.followers.add(follower)
        return Response({"type": "follower", "detail": "Follower added and friend request accepted."}, status=status.HTTP_200_OK)

    def delete(self, request, user_id, follower_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        follower = get_object_or_404(AppUser, pk=follower_id)
        user.followers.remove(follower)
        return Response({"type": "follower", "detail": "Follower removed."}, status=status.HTTP_200_OK)


class FriendRequestList(APIView):
    def get(self, request, user_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        friend_requests = FriendRequest.objects.filter(object=user)
        data = FriendRequestSerializer(friend_requests, many=True).data
        for request in data:
            request['accepted'] = friend_requests.get(id=request['id']).accepted
        return Response({"type": "friendRequestsReceived", "items": data}, status=status.HTTP_200_OK)

class SentFriendRequestList(APIView):
    """List all friend requests sent by a given user."""

    def get(self, request, user_id, format=None):
        user = get_object_or_404(AppUser, pk=user_id)
        print('user in backedn', user)
        sent_requests = FriendRequest.objects.filter(actor=user)
        print('sent requsts, ', sent_requests)
        serializer = FriendRequestSerializer(sent_requests, many=True)
        print('sent back to frotn end', serializer.data)
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
