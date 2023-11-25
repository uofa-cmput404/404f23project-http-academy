from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
# from .models import AppUser, FriendRequest
from authors.models import AppUser
from followers.models import FriendRequest

class FollowersTestCase(TestCase):

    def setUp(self):
        # Setting up test users
        self.user1 = AppUser.objects.create_user(username='user1', email='user1@example.com', password='password')
        self.user2 = AppUser.objects.create_user(username='user2', email='user2@example.com', password='password')

        # Creating a friend request
        self.friend_request = FriendRequest.objects.create(actor=self.user1, object=self.user2, summary="Test Friend Request")

        # Setting up the client
        self.client = APIClient()

    def test_friend_request_creation(self):
        # Testing creation of FriendRequest
        self.assertEqual(FriendRequest.objects.count(), 1)
        self.assertEqual(self.friend_request.actor, self.user1)
        self.assertEqual(self.friend_request.object, self.user2)

    def test_followers_relationship(self):
        # Testing followers relationship 
        
        '''
        1. add user1 in followers list of user2 
        2. check if users is in the followers list 
        '''
        self.user1.followers.add(self.user2)
        self.assertIn(self.user2, self.user1.followers.all())

    # def test_follower_list_view(self):
    #     # Testing the FollowerList view
    #     url = reverse('followers-list', kwargs={'user_id': self.user1.user_id})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accept_friend_request_view(self):
        # Testing the AcceptFriendRequest view
        # print('users', type(self.user1.user_id))
        # print('users', type(self.user2.user_id))
        
        
        # url = reverse('accept-friendrequest', kwargs={'user_id': self.user2.user_id, 'requester_id': str(self.user1.user_id)})
        # print('url', url)
        
        
        
        # response = self.client.post(url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.user2.refresh_from_db()
        # self.assertIn(self.user1, self.user2.followers.all())

    # def test_accept_nonexistent_friend_request(self):
    #     # Testing acceptance of a non-existent friend request
    #     non_existent_user_id = 999
    #     url = reverse('accept-friendrequest', kwargs={'user_id': non_existent_user_id, 'requester_id': self.user1.user_id})
    #     response = self.client.post(url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

   

