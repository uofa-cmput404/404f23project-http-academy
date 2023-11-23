from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
from django.test import TestCase
from django.urls import reverse

class PostTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(email='testemail', password='testpassword')

        # Force the test user to login without authentication
        self.client.force_login(self.user)
    
    def createTestPost(self):
        return Post.objects.create(author=self.user, title="Test Post", content="Test Content", image="", unlisted=True)

    def createTestComment(self):
        post = self.createTestPost()
        return Comment.objects.create(author=self.user, comment="Test Comment", postId=post)
    
    def createTestLike(self):
        post = self.createTestPost()
        return Like.objects.create(author=self.user, postId=post)

    def test_get_all_posts(self):
        first_response = self.client.get(reverse("posts:posts"))
        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(len(first_response.data), 0)

        self.createTestPost()
        second_response = self.client.get(reverse("posts:posts"))
        self.assertEqual(len(second_response.data), 1)

    def test_post_a_post(self):
        data = {
            'title': 'This is a test title',
            'content': 'This is test content',
            'unlisted': True,
            'author': 1,
        }
        response = self.client.post(reverse("posts:posts"), data)
        id = response.data["id"]
        retrieved_post = Post.objects.filter(id=1)
        self.assertEqual(id, retrieved_post[0].id)

    def test_get_a_specific_post(self):
        created_post = self.createTestPost()
        id = created_post.id
        response = self.client.get(reverse("posts:post_detail", args=[created_post.pk]))
        retrieved_post = response.data
        self.assertEqual(id, retrieved_post["id"])

    def test_delete_a_post(self):
        post = self.createTestPost()
        self.assertEqual(Post.objects.count(), 1)
        response = self.client.delete(reverse('posts:post_detail', args=[post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 0)

    def test_get_all_comments_for_post(self):
        first_response = self.client.get(reverse("posts:comments_list", args=[1]))
        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(len(first_response.data), 0)
        comment = self.createTestComment()
        second_response = self.client.get(reverse("posts:comments_list", args=[comment.pk]))
        self.assertEqual(len(second_response.data), 1)

    def test_post_new_commentt(self):
        post = self.createTestPost()
        self.assertEquals(Comment.objects.filter(postId=post.id).__len__(), 0)
        data = {
            'author': 1,
            'comment': 'This is a test comment',
            'postId': post.id,
        }
        response = self.client.post(reverse("posts:comments_list", args=[post.id]), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.filter(postId=post.id).__len__(), 1)
    
    def test_get_specific_comment(self):
        created_comment = self.createTestComment()
        response = self.client.get(reverse("posts:comment_detail", args=[created_comment.pk]))
        self.assertEqual(response.status_code, 200)
        retrieved_comment_id = response.data["id"]
        self.assertEqual(created_comment.id, retrieved_comment_id)

    def test_delete_a_comment(self):
        self.createTestComment()
        self.assertEqual(Comment.objects.filter().__len__(), 1)
        response = self.client.delete(reverse("posts:comment_detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.filter().__len__(), 0)

    def test_get_all_likes_for_a_post(self):
        first_response = self.client.get(reverse("posts:like_post", args=[1]))
        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(len(first_response.data), 0)
        self.createTestLike()
        second_response = self.client.get(reverse("posts:like_post", args=[1]))
        self.assertEqual(len(second_response.data), 1)

    # def test_delete_a_like(self):
    #     self.createTestLike()
    #     self.assertEqual(Like.objects.filter().__len__(), 1)
    #     response = self.client.delete(reverse("posts:like_post", args=[1]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Like.objects.filter().__len__(), 0)

    def test_create_a_like(self):
        post = self.createTestPost()
        self.assertEqual(Like.objects.filter().__len__(), 0)
        data = {
            'author': 1,
            'post': 1
        }
        response = self.client.post(reverse("posts:like_post", args=[post.id]), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.filter().__len__(), 1)

    def test_get_image(self):
        base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAWklEQVR42mNkAAIAAAoAAv/lxKUAAAAASUVORK5CYII="
        post = Post.objects.create(author=self.user, title="Test Post", content="Test Content", image=base64, unlisted=True)
        response = self.client.get(reverse("posts:get_post_image", args=[post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(base64, response.data)