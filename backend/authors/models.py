# from django.db import models
# from django.contrib.postgres.fields import ArrayField
# from django.contrib.auth.models import User
# import uuid
# # Create your models here.

# class Author(models.Model):
    

#     user = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, null = True)
#     type = models.CharField(max_length=6, blank = True, null = True)
#     author_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank = True)
#     id = models.URLField(max_length=2048, null = True)
#     displayName = models.CharField(max_length = 140, null = True)
#     github = models.URLField(blank = True, null = True)
#     profileImage = models.URLField(blank = True, null = True)
    

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse

class AppUserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		user = self.model(email=email)
		user.set_password(password)
		user.is_superuser = False
		user.is_staff = False
		user.save()
		return user
	
	def create_superuser(self, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.create_user(email, password)
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return user

from django.contrib.auth.models import Group, Permission
'''
class AppUser(AbstractBaseUser, PermissionsMixin):

    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50)
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

    def __str__(self):
        return self.username
'''
class AppUser(AbstractBaseUser, PermissionsMixin):
    
    type = models.CharField(max_length=6, blank = True, null = True)
    user_id = models.AutoField(primary_key=True)
	

    username = models.CharField(max_length=140, null = True)
    email = models.EmailField(max_length=50, unique=True) # remove this later
    
    github = models.URLField(blank = True, null = True)
    profileImage = models.URLField(blank = True, null = True)
    
	
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


    def get_absolute_url(self):
        # Assuming you have a URL pattern named 'author-detail' in your urls.py
        return reverse('user-detail', args=[str(self.pk)])

def __str__(self):
    return self.username