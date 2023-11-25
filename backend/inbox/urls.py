from django.contrib import admin
from django.urls import path, include
from .views import InboxView
from rest_framework import routers



urlpatterns = [
    path('', InboxView.as_view(), name='inbox-detail') # GET inbox of a user 

]
