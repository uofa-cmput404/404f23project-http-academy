from django.db import models

# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    displayName = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    profileImage = models.CharField(max_length=100)