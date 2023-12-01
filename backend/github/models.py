from django.db import models
from authors.models import AppUser
from django.utils import timezone
import uuid
from posts.models import Post



class GitHubFeed(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

