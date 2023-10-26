from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    published = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    caption = models.TextField(max_length=150, null=True)
    image = models.TextField(null=True)
    contentType = models.CharField(max_length=20, default='text/plain')
    categories = models.ForeignKey('Category', on_delete=models.CASCADE, default=None, null=True)
    count = models.IntegerField(default=0)
    comments = models.ForeignKey('Comment', on_delete=models.CASCADE, default=None, null=True)
    likes = models.IntegerField(default=0)
    visibility = models.CharField(max_length=100, default='PUBLIC')
    unlisted = models.BooleanField()


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    comment = models.CharField(max_length=100)
    contentType = models.CharField(max_length=100, default='text/plain')
    published = models.DateTimeField(auto_now_add=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE, db_index=True)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100)
    linkedPost = models.ForeignKey(Post, on_delete=models.CASCADE)