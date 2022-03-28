from django.shortcuts import render

__all__ = ['index']


def index(request):
    return render(request, 'index.html')
