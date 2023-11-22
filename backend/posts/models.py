from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from authors.models import AppUser
# Create your models here.


DEFAULT_HOST = "http://127.0.0.1:8000/"


import uuid
class Post(models.Model):
    
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.URLField(max_length=2048, blank=True, null=True, editable=False)
    author = models.ForeignKey(AppUser, related_name="post_user", on_delete=models.CASCADE, db_index=True)
    published = models.DateTimeField(auto_now_add=True)
    type = models.CharField(default="post",max_length=4, editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=150, null=True)
    image = models.TextField(null=True, blank = True)
    count = models.IntegerField(default=0,blank=True,null=True)
    source = models.URLField(max_length=500,default=DEFAULT_HOST)
    origin = models.URLField(max_length=500,default=DEFAULT_HOST)
    contentType = models.CharField(max_length=20, default='text/plain')
    categories = models.ForeignKey('Category', on_delete=models.CASCADE, default=None, null=True)
    comments = models.ForeignKey('Comment', on_delete=models.CASCADE, default=None, null=True)
    likes = models.ForeignKey('Like', on_delete=models.CASCADE, default=None, null=True)
    visibility = models.CharField(max_length=100, default='PUBLIC')
    unlisted = models.BooleanField()
    url = models.URLField(max_length=500,editable=False,null=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE, db_index=True)
    comment = models.CharField(max_length=100)
    contentType = models.CharField(max_length=100, default='text/plain')
    published = models.DateTimeField(auto_now_add=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE, db_index=True)


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE, db_index=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE, db_index=True, null=True)
    commentId = models.ForeignKey(Comment, on_delete=models.CASCADE, db_index=True, null=True)
    like = models.IntegerField(default=0)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100)
    linkedPost = models.ForeignKey(Post, on_delete=models.CASCADE)
