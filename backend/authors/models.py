from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class author(models.Model):
    id = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    displayName = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    profileImage = models.CharField(max_length=100)
    user_id = models.AutoField(primary_key=True)
    