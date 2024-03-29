from .views import *
from django.urls import path

urlpatterns = [
    path('', ChatViewset.as_view(), name='chats'),
    path('<int:id>/', ChatView.as_view(), name='chat'),
    path('<int:chat_id>/member/<int:user_id>/', MemberView.as_view(), name='member'),
    path('<int:chat_id>/message/', MessageViewSet.as_view(), name='messages'),
    path('<int:chat_id>/message/<int:id>/', MessageView.as_view(), name='message'),
    path('private/<str:username>/', PerformPrivateChatView.as_view(), name='private_chat'),
    path('read_message/<int:id>/', ReadMessageView.as_view(), name='read_message'),
]
