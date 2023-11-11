from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from authors.models import AppUser
# Create your models here.

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE, db_index=True)
    published = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=150, null=True)
    image = models.TextField(null=True)
    contentType = models.CharField(max_length=20, default='text/plain')
    categories = models.ForeignKey('Category', on_delete=models.CASCADE, default=None, null=True)
    count = models.IntegerField(default=0)
    comments = models.ForeignKey('Comment', on_delete=models.CASCADE, default=None, null=True)
    likes = models.ForeignKey('Like', on_delete=models.CASCADE, default=None, null=True)
    visibility = models.CharField(max_length=100, default='PUBLIC')
    unlisted = models.BooleanField()


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    comment = models.CharField(max_length=100)
    contentType = models.CharField(max_length=100, default='text/plain')
    published = models.DateTimeField(auto_now_add=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE, db_index=True)


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE, db_index=True, null=True)
    commentId = models.ForeignKey(Comment, on_delete=models.CASCADE, db_index=True, null=True)
    like = models.IntegerField(default=0)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100)
    linkedPost = models.ForeignKey(Post, on_delete=models.CASCADE)
