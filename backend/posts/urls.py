# from django.contrib import admin
# from django.urls import path, include
# from . import views
# from rest_framework import routers

# app_name = 'posts'
# # TODO: update these routes as per project requirements
# urlpatterns = [
#     path('', views.posts_list), # GET all posts, POST a new post
#     path('posts/<int:pk>/', views.posts_list, name='author_posts_list'), # GET all or public posts of a specific author
#     path('<str:pk>', views.post_detail, name = 'post_detail'), # GET a specific post, DELETE a post
#     path('<str:pk>/comments/', views.comments_list), # GET all comments for a post, POST a new comment
#     path('comments/<str:pk>', views.comment_detail), # GET a specific comment, DELETE a comment
#     path('<str:pk>/like/', views.like_post), # GET all likes for a post, POST a like, DELETE a like
#     path('<str:pk>/like/<str:pkLike>', views.like_detail), # GET a specific like to delete
#     path('<str:pk>/image/', views.get_post_image) # GET the image for a post
# ]


from django.urls import path, re_path
from . import views
from django.conf.urls import include
from rest_framework import routers

app_name = 'posts'

urlpatterns = [

    path('', views.posts_list), # GET all posts, POST a new post
    path('ownPosts/', views.own_posts_list), # GET all posts, POST a new post for a specific author
    # path('<uuid:pk>/', views.posts_list, name='author_posts_list'), # GET all or public posts of a specific author
    # path('<uuid:post_id>/', views.post_detail, name='post_detail'), # GET a specific post, DELETE a post
    path('<uuid:post_id>/comments/', views.comments_list), # GET all comments for a post, POST a new comment
    # path('comments/<uuid:pk>', views.comment_detail), # GET a specific comment, DELETE a comment
    # path('<uuid:pk>/like/', views.like_post), # GET all likes for a post, POST a like, DELETE a like
    # path('<uuid:pk>/like/<uuid:pkLike>', views.like_detail), # GET a specific like to delete
    path('<uuid:pk>/image/', views.get_post_image), # GET the image for a post
    # path('<uuid:author_id>/posts/<int:post_id>/', views.post_detail, name='post_detail')
    path('<uuid:post_id>/', views.post_detail, name='author_post_detail'),
    path('<uuid:post_id>/like/', include('like.urls')),
    # path('<uuid:comment_id>/like/', include('like.urls')),
    path('comments/<uuid:comment_id>/likes/', views.comment_like),
    path('search/<str:query>', views.search_posts)
]
