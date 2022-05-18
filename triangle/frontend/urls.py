from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    path('user/<str:username>', about_user),
    path('<str:username>/reset/<str:key>', reset_password),
    path('chats', chats_page),
    path('contacts', contacts_page)
]
