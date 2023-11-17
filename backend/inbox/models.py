from django.db import models
from authors.models import AppUser
from posts.models import Post, Like 
from followers.models import FriendRequest
# Create your models here.
class Inbox(models.Model):

    authorId = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    
    type = models.CharField(max_length=100)
    
    posts = models.ManyToManyField(Post, blank = True)

    follow_request = models.ManyToManyField(FriendRequest, blank = True)

    like = models.ManyToManyField(Like, blank = True)