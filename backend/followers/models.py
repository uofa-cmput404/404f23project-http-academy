"""Contains the models for the follower app."""

from django.db import models
import uuid
from authors.models import AppUser


class FriendRequest(models.Model):
   
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    type = models.CharField(default='Follow', max_length=6, editable=False)

    summary = models.CharField(max_length=100)

    actor = models.ForeignKey(AppUser, related_name = 'sent_friend_request', on_delete = models.CASCADE, default ='')

    object = models.ForeignKey(AppUser, related_name = 'recieved_friend_request', on_delete = models.CASCADE, default ='')

    accepted = models.BooleanField(default=False)
    class Meta:
        # allow one friend request from one user to the another user
        constraints = [models.UniqueConstraint(fields=['actor','object'],name='unique_request')]
