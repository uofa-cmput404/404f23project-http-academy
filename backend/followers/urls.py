
from django.conf.urls import include
from django.urls import path
from . import views

urlpatterns = [
    # URL for listing all followers of a specific user
    path('', views.FollowerList.as_view(), name='followers-list'),
    
    
    # URL for managing a specific follower of a user (check, add, delete).
    path('<uuid:follower_id>/', views.FollowerDetail.as_view(), name='follower-detail'),
    
    path('acceptFriend/<uuid:requester_id>/', views.AcceptFriendRequest.as_view(), name='accept-follower'),
    path('removeFriend/<uuid:requester_id>/', views.UnfriendUser.as_view(), name='accept-follower'),


    # URL for listing all friend requests for a specific user
    path('friendrequests/', views.FriendRequestList.as_view(), name='friendrequest-list'),
    
    #url for checking if user has sent a friend request 
    path('sentFriendRequests/', views.SentFriendRequestList.as_view(), name='sent-friendrequestlist'),

    # URL for managing a specific friend request (check, add, delete)
    path('friendrequests/<str:requester_id>/', views.FriendRequestDetail.as_view(), name='friendrequest-detail'),

    path('acceptFriendRequest/<int:user_id>/<str:requester_id>/', views.AcceptFriendRequest.as_view(), name='accept-friendrequest'),
    path('establishMutualFriendship/<uuid:friend_id>/', views.EstablishMutualFriendship.as_view(), name='establish-mutual-friendship'),
]
