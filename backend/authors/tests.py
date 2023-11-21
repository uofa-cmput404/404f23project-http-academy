from django.test import TestCase
from .models import AppUser, Follower, FollowRequest


class FollowerModelTest(TestCase):
    def setUp(self):
        self.user1 = AppUser.objects.create(username='testuser1', email='test1@gmail.com')
        self.user2 = AppUser.objects.create(username='testuser2', email='test2@gmail.com')
        self.follower = Follower.objects.create(author=self.user1, follower=self.user2)

    def test_follower_author(self):
        self.assertEqual(self.follower.author, self.user1)

    def test_follower_follower(self):
        self.assertEqual(self.follower.follower, self.user2)

    def test_follower_str(self):
        self.assertEqual(str(self.follower), 'testuser2 follows testuser1')

    def test_follower_unique(self):
        with self.assertRaises(Exception):
            Follower.objects.create(author=self.user1, follower=self.user2)

    def test_follower_delete(self):
        self.follower.delete()
        self.assertEqual(len(Follower.objects.all()), 0)

    def test_follower_delete_author(self):
        self.user1.delete()
        self.assertEqual(len(Follower.objects.all()), 0)


class FollowRequestModelTest(TestCase):
    def setUp(self):
        self.user1 = AppUser.objects.create(username='testuser1', email='test1@gmail.com')
        self.user2 = AppUser.objects.create(username='testuser2', email='test2@gmail.com')
        self.follow_request = FollowRequest.objects.create(object=self.user1, actor=self.user2)

    def test_follow_request_object(self):
        self.assertEqual(self.follow_request.object, self.user1)

    def test_follow_request_actor(self):
        self.assertEqual(self.follow_request.actor, self.user2)

    def test_follow_request_str(self):
        self.assertEqual(str(self.follow_request), 'testuser2 requested to follow testuser1')

    def test_follow_request_unique(self):
        with self.assertRaises(Exception):
            FollowRequest.objects.create(object=self.user1, actor=self.user2)

    def test_follow_request_delete(self):
        self.follow_request.delete()
        self.assertEqual(len(FollowRequest.objects.all()), 0)

    def test_follow_request_delete_object(self):
        self.user1.delete()
        self.assertEqual(len(FollowRequest.objects.all()), 0)