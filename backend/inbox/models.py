from django.db import models
from authors.models import AppUser
from posts.models import Post

# Create your models here.
class Inbox(models.Model):

    authorId = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    postId = models.ManyToManyField(Post)