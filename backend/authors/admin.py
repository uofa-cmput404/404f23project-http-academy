from django.contrib import admin

# Register your models here.

from .models import AppUser, AppUserManager

# Register your models here.
admin.site.register(AppUser)