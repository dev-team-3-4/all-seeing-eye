from django.shortcuts import render
from django.http import HttpResponseNotFound
from http.cookies import SimpleCookie
from rest_framework.authtoken.models import Token

__all__ = ['index', 'about_user', 'reset_password', 'chats_page', 'contacts_page', 'search_contacts_page']

from users.models import User


def index(request):
    return render(request, 'index.html')


def about_user(request, username):
    founded_user = User.objects.filter(username=username)

    if not founded_user.exists():
        return HttpResponseNotFound("Пользователь с таким именем не найден!")
    founded_user = founded_user[0]  # TODO: Костыль, надо пофиксить

    cookie = SimpleCookie()
    cookie.load(request.headers['cookie'])
    logged_username = cookie['username'].value

    logged_user = Token.objects.get(key=cookie['token'].value).user

    if username == logged_username:
        return render(request, 'user.html', {
            "username": founded_user.username,
            "user_email": founded_user.email,
            "card_number": founded_user.bank_card_number,
            "profile_picture_url": founded_user.profile_photo,
            "self_page": True,
            "online": "Online" if founded_user.is_online else "Offline"
        })
    return render(request, 'user.html', {
        "already_in_contacts": logged_user.contacts.contains(founded_user),
        "username": founded_user.username,
        "user_email": founded_user.email,
        "self_page": False,
        "online": "Online" if founded_user.is_online else "Offline"
    })


def reset_password(request, username, key):
    return render(request, "reset_password.html", {"username": username, "key": key})


def chats_page(request):
    return render(request, "chats.html")


def contacts_page(request):
    return render(request, 'contacts.html')


def search_contacts_page(request):
    return render(request, 'search_contacts.html')
