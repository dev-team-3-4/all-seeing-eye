from django.shortcuts import render
from django.http import HttpResponseNotFound

__all__ = ['index', 'about_user', 'reset_password', 'chats_page', 'contacts_page']

from users.models import User


def index(request):
    return render(request, 'index.html')


def about_user(request, username):
    founded_user = User.objects.filter(username=username)

    if not founded_user.exists():
        return HttpResponseNotFound("Пользователь с таким именем не найден!")
    founded_user = founded_user[0]  # TODO: Костыль, надо пофиксить

    return render(request, 'user.html', {
        "username": founded_user.username,
        "user_email": founded_user.email,
        "card_number": founded_user.bank_card_number,
        "profile_picture_url": founded_user.profile_photo
    })


def reset_password(request, username, key):
    return render(request, "reset_password.html", {"username": username, "key": key})


def chats_page(request):
    return render(request, "chats.html")


def contacts_page(request):
    return render(request, 'contacts.html')
