

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse
import uuid
from django.contrib.auth.models import Group, Permission

DEFAULT_HOST = "http://127.0.0.1:8000/"

class AppUserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.is_superuser = False
		user.is_staff = False
		user.save()
		return user
	
	def create_superuser(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.create_user(email, password, **extra_fields)
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    
    type = models.CharField(default ="author", max_length=6, blank = True, null = True)
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	
    #host + id
    id = models.URLField(max_length=2048, blank=True, null=True)
    username = models.CharField(max_length=140, null = True)
    email = models.EmailField(max_length=50, unique=True) # remove this later
    #url link to user profile
    url = models.URLField(blank=True, null=True, editable=False)
    github = models.URLField(blank = True, null = True)
    profileImage = models.URLField(blank = True, null = True)
    
    host = models.URLField(blank=True, default=DEFAULT_HOST, null=True)

    displayName = models.CharField(max_length=100, blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followed_by',
        blank=True
    )
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='follows',
        blank=True
    )
    
	
    is_staff = models.BooleanField(default=False)  # Add this field to indicate staff status
    groups = models.ManyToManyField(
        Group,
        related_name='app_users',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='app_users',
        blank=True,
    )
    USERNAME_FIELD = 'email'

    objects = AppUserManager()


    def create_url(self):
        if not self.host.endswith("/"):
            self.host += "/"
        return f"{self.host}authors/{self.user_id}"

    def save(self, *args, **kwargs):
        self.url = self.create_url()
        self.id = self.url
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Assuming you have a URL pattern named 'author-detail' in your urls.py
        return reverse('user-detail', args=[str(self.pk)])
def __str__(self):
    return self.username