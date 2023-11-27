from django.test import TestCase
from django.urls import reverse
from authors.models import AppUser
from .models import Inbox, Post, FriendRequest, Like
from .views import InboxView
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, force_authenticate

# Create your tests here.
class InboxTests(TestCase):
  def setUp(self):
    # Create users
    self.user1 = AppUser.objects.create_user(email='test@email.com', password='test1234')
    self.user2 = AppUser.objects.create_user(email='test1@email.com', password='test1234')

    # Force authentication
    self.client.force_login(self.user1)
    self.client.force_login(self.user2)

    # Create inbox
    self.inbox = Inbox.objects.create(authorId=self.user1)

    # Create API factory
    self.factory = APIRequestFactory()

  def test_add_post_to_inbox(self):
    user = str(self.user1)
    request = self.factory.get('/inbox/' + user)
    force_authenticate(request, self.user1)
    response = InboxView.as_view()(request, author_id = self.user1.user_id)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["type"], "inbox")
    self.assertEqual(len(response.data['posts']), 0)

    post = Post.objects.create(author=self.user1, title="Test Post", content="Test Content", image="", unlisted=True)
    self.inbox.posts.add(post)
    print("Inbox: ", self.inbox.posts)
    #self.assertEqual(len(response.data['posts']), 1)

  def test_follow_request_in_inbox(self):
    fr = FriendRequest.objects.create(actor=self.user1, object=self.user2)
    
    user = str(self.user1)
    request = self.factory.get('/inbox/' + user)
    force_authenticate(request, self.user1)
    response = InboxView.as_view()(request, author_id = self.user1.user_id)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["type"], "inbox")
    #self.assertEqual(len(response.data['follow_request']), 1)

  def test_add_like_to_inbox(self):
    user = str(self.user1)
    request = self.factory.get('/inbox/' + user)
    force_authenticate(request, self.user1)
    response = InboxView.as_view()(request, author_id = self.user1.user_id)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["type"], "inbox")
    #self.assertEqual(len(response.data['like']), 0)

    like = Like.objects.create(author=self.user1)
    self.inbox.like.add(like)
    #self.assertEqual(len(response.data['like']), 1

  def test_like_in_inbox(self):
    like = Like.objects.create(author=self.user1)
    self.inbox.like.add(like)

    user = str(self.user1)
    request = self.factory.get('/inbox/' + user)
    force_authenticate(request, self.user1)
    response = InboxView.as_view()(request, author_id = self.user1.user_id)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["type"], "inbox")
    #self.assertEqual(len(response.data['like']), 1)

def test_extract_uuid_from_url(self):
    url = "http://" + self.user1.host + "/author/" + str(self.user1.user_id)
    uuid = InboxView.extract_uuid_from_url(url)
    self.assertEqual(uuid, str(self.user1.user_id))

  

