from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    path('userabout', userabout),
    path('<str:username>/reset/<str:key>', reset_password)
]
