from django.contrib import admin

# Register your models here.

from .models import AppUser, AppUserManager, Follower

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Follower)