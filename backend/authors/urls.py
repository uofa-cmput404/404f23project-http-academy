from django.contrib import admin
from django.urls import path, include
from like.views import LikedView
from . import views
from followers.views import FollowingList
from rest_framework import routers


# app_name = 'authors'
urlpatterns = [
	path('register', views.UserRegister.as_view(), name='register'),
	path('login', views.UserLogin.as_view(), name='login'),
	path('logout', views.UserLogout.as_view(), name='logout'),
	path('user', views.UserView.as_view(), name='user'),
	
	path('<uuid:pk>/update/', views.UserUpdate.as_view(), name='user-update'),
	path('<uuid:pk>/', views.UserDetails.as_view(), name='user-detail'),
	# path('<int:pk>/inbox/', include('inbox.urls')),
	# path('<int:pk>/inbox/', views.test_work.as_view(), name="inbox")
	path('<uuid:pk>/posts/', include('posts.urls'), name="authors-posts"),
	path('<uuid:author_id>/inbox/', include('inbox.urls')),
	path('<uuid:user_id>/followers/', include('followers.urls'), name="followers"),
    path('<uuid:user_id>/following/', FollowingList.as_view(), name='following-list'),

    path('<uuid:author_id>/liked/', LikedView.as_view(), name="author-liked"),
    # path('get-csrf-token/', views.csrf_token, name='get-csrf-token'),
]