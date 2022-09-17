from django.urls import path
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
    path('create_deal/<int:deal_id>', create_deal),
    path('input_deal/<int:deal_id>', input_deal),
    path('invite_moderator/<int:deal_id>', invite_moderator),
    path('invites', invites_page)
]
