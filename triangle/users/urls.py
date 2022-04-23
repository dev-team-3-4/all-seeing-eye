from .views import *
from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('', UserViewSet.as_view()),
    path('token/', ObtainAuthToken.as_view()),
    path('confirm_email/', EmailConfirmView.as_view()),
    path('<str:username>/reset_password/', PasswordResetView.as_view()),
]
