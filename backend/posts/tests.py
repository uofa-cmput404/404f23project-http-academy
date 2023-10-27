from django.test import TestCase

# Create your tests here.
# TODO: add tests for posts
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Post

class LikePostTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # TODO: this won't work until we have the user model set up (Jefferson)
        self.post = Post.objects.create(
            author='1',
            title='Test Post', 
            content='Test Content',
            isPublic=True,
            unlisted=False
            )

    def test_like_post(self):
        url = reverse('like_post', args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Post liked successfully')
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes, 1)

    def test_unlike_post(self):
        self.post.likes = 1
        self.post.save()
        url = reverse('like_post', args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Post unliked successfully')
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes, 0)

    def test_get_likes(self):
        self.post.likes = 2
        self.post.save()
        url = reverse('like_post', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 2)