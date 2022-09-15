from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    path('user/<str:username>', about_user),
    path('<str:username>/reset/<str:key>', reset_password),
    path('chats', chats_page),
    path('contacts', contacts_page),
    path('search_contacts', search_contacts_page),
    path('chat/<int:chat_id>', chat_with_users_page),
    path('create_chat', create_chat),
    path('deals', contracts_list),
    path('create_deal', create_deal),
]
