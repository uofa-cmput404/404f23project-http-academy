from django.contrib import admin

# Register your models here.

from .models import AppUser, AppUserManager, Follower, FollowRequest

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Follower)
admin.site.register(FollowRequest)