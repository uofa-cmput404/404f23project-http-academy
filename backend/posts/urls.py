from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'posts'
# TODO: update these routes as per project requirements
urlpatterns = [
    path('', views.posts_list), # GET all posts, POST a new post
    path('<str:pk>', views.post_detail), # GET a specific post, DELETE a post
    path('<str:pk>/comments/', views.comments_list), # GET all comments for a post, POST a new comment
    path('comments/<str:pk>', views.comment_detail), # GET a specific comment, DELETE a comment
    path('<str:pk>/like/', views.like_post), # GET all likes for a post, POST a like, DELETE a like
    
]
