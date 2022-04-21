from django.urls import path
from . import views
urlpatterns=[
    path('', views.Home, name='Home'),
    path('room/<str:pk>/', views.Room, name='room'),
]