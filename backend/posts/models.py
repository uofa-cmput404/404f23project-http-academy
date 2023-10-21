from django.db import models

# Create your models here.
# please use only restful interface for coding

class User(models.Model):
    id = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    displayName = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    profileImage = models.CharField(max_length=100)
    user_id = models.AutoField(primary_key=True)

class Post(models.Model):
    title = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    contentType = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.CharField(max_length=100)
    count = models.IntegerField()
    size = models.IntegerField()
    next = models.CharField(max_length=100)
    previous = models.CharField(max_length=100)
    visibility = models.CharField(max_length=100)
    unlisted = models.BooleanField()
    published = models.DateTimeField()
    id = models.CharField(max_length=100, primary_key=True)
    post_id = models.AutoField(primary_key=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    contentType = models.CharField(max_length=100)
    published = models.DateTimeField()
    id = models.CharField(max_length=100, primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_id = models.AutoField(primary_key=True)


