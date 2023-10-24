from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'posts'
# TODO: update these routes as per project requirements
urlpatterns = [
    path('', views.posts_list),
    path('<str:pk>', views.post_detail),
    path('<str:pk>/comments/', views.comments_list),
    path('comments/<str:pk>', views.comment_detail),
    path('<str:pk>/like/', views.like_post),
]
