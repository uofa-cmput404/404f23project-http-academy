from django.urls import path

from .views import LikesView

urlpatterns = [
    path('', LikesView.as_view(), name="like"),
]