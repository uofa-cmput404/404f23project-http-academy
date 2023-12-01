from django.urls import path
from .views import GitHubFeedList

urlpatterns = [
    path('github-feeds/', GitHubFeedList.as_view(), name='github-feeds'),
]