from django.shortcuts import render

__all__ = ['index', 'userabout', 'reset_password']


def index(request):
    return render(request, 'index.html')


def userabout(request):
    return render(request, 'user.html')  # Временная херня


def reset_password(request, username, key):
    return render(request, "reset_password.html", {"username": username, "key": key})