from django.shortcuts import render
from django.http import HttpResponseNotFound
from http.cookies import SimpleCookie
from rest_framework.authtoken.models import Token

__all__ = ['index', 'about_user', 'reset_password', 'chats_page', 'contacts_page',
           'search_contacts_page', 'chat_with_users_page', 'create_chat', 'contracts_list', 'create_deal', 'input_deal',
           'invite_moderator']

from chats.models import Chat
from users.models import User


def index(request):
    return render(request, 'index.html')


def about_user(request, username):
    return render(request, 'user.html')


def reset_password(request, username, key):
    return render(request, "reset_password.html", {"username": username, "key": key})


def chats_page(request):
    return render(request, "chats.html")


def contacts_page(request):
    return render(request, 'contacts.html')


def search_contacts_page(request):
    return render(request, 'search_contacts.html')


def chat_with_users_page(request, chat_id: int):
    return render(request, "chat.html", {"chat_id": chat_id})


def create_chat(request):
    return render(request, "create_chat.html")


def contracts_list(request):
    return render(request, "contracts_list.html")


def create_deal(request, deal_id: int):
    return render(request, "create_deal.html")


def input_deal(request, deal_id: int):
    return render(request, "append_deal.html")


def invite_moderator(request, deal_id: int):
    return render(request, "add_moderator.html")
