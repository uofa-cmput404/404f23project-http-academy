from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'authors'
urlpatterns = [
    path('', views.authors_list),
    path('<str:pk>/', views.authors_detail),
]