from .views import *
from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('', UserViewSet.as_view()),
    path('token/', ObtainAuthToken.as_view()),
    path('change/email/', EmailConfirmView.as_view()),
    path('<str:username>/reset/', PasswordResetView.as_view()),
    path('<str:username>/change/password/', ChangePasswordView.as_view()),
]
