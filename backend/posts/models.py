import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from authors.models import AppUser
# Create your models here.


DEFAULT_HOST = "http://127.0.0.1:8000/"


class Post(models.Model):

    post_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    id = models.URLField(max_length=2048, blank=True,
                         null=True, editable=False)
    author = models.ForeignKey(
        AppUser, related_name="post_user", on_delete=models.CASCADE, db_index=True)
    published = models.DateTimeField(auto_now_add=True)
    isForeign = models.BooleanField(default=False)
    type = models.CharField(default="post", max_length=4, editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=150, null=True)
    image = models.TextField(null=True, blank=True)
    count = models.IntegerField(default=0, blank=True, null=True)
    source = models.URLField(max_length=500, default=DEFAULT_HOST)
    origin = models.URLField(max_length=500, default=DEFAULT_HOST)
    contentType = models.CharField(max_length=20, default='text/plain')
    categories = models.ForeignKey(
        'Category', on_delete=models.CASCADE, default=None, null=True)
    foreign = models.UUIDField(default=uuid.uuid4, editable=True)
    comments = models.ForeignKey(
        'Comment', on_delete=models.CASCADE, default=None, null=True)

    likes = models.ForeignKey(
        'Like', on_delete=models.CASCADE, default=None, null=True)
    visibility = models.CharField(max_length=100, default='PUBLIC')
    unlisted = models.BooleanField()
    url = models.URLField(max_length=500, editable=False, null=True)
    # comments = models.URLField(max_length=500,editable=False,default=str(url) + '/comments')

    def save(self, *args, **kwargs):

        # If the user is not foreign, use the user_id as part of the URL
        if not self.author.isForeign:
            print('got hre to create post')
            self.foreign = self.post_id

        super().save(*args, **kwargs)


class Comment(models.Model):

    CONTENT_CHOICE = [
        ("text/markdown", "text/markdown"),
        ("text/plain", "text/plain"),
        ("application/base64", "application/base64"),
        ("image/png;base64", "image/png;base64"),
        ("image/jpeg;base64", "image/jpeg;base64")
    ]

    comment_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    id = models.URLField(max_length=2048, blank=True,
                         null=True, editable=False)
    author = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, db_index=True)
    comment = models.TextField()
    contentType = models.CharField(
        max_length=100, choices=CONTENT_CHOICE, default='text/plain')
    published = models.DateTimeField(auto_now_add=True)
    postId = models.ForeignKey(
        Post, on_delete=models.CASCADE, db_index=True, related_name="comment_for_post")
    url = models.URLField(max_length=500, editable=False,
                          null=True, blank=True)
    isForeign = models.BooleanField(default=False)
    foreign = models.UUIDField(default=uuid.uuid4, editable=True)

    def save(self, *args, **kwargs):
        if not self.author.isForeign:
            self.foreign = self.comment_id
            self.url = str(self.postId.id) + "comments/" + str(self.comment_id)
            self.id = self.url
        super().save(*args, **kwargs)


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, db_index=True)
    postId = models.ForeignKey(
        Post, on_delete=models.CASCADE, db_index=True, null=True)
    commentId = models.ForeignKey(
        Comment, on_delete=models.CASCADE, db_index=True, null=True)
    like = models.IntegerField(default=0)
    isForeign = models.BooleanField(default=False)
    foreign = models.UUIDField(default=uuid.uuid4, editable=True)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100)
    linkedPost = models.ForeignKey(Post, on_delete=models.CASCADE)
