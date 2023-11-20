from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
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
        if self.username is None:
            return self.email
        return self.username
	

class Follower(models.Model):
    author = models.ForeignKey(AppUser, related_name='author', on_delete=models.CASCADE, db_index=True)
    follower = models.ForeignKey(AppUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'follower')

    def __str__(self):
        return f"{self.follower} follows {self.author}"
	

class FollowRequest(models.Model):
    object = models.ForeignKey(AppUser, related_name='author_request', on_delete=models.CASCADE, db_index=True)
    actor = models.ForeignKey(AppUser, related_name='follow_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('object', 'actor')

    def __str__(self):
        return f"{self.actor} requested to follow {self.object}"