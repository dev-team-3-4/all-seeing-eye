from .views import *
from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('', UserViewSet.as_view()),
    path('token/', ObtainAuthToken.as_view()),
    path('confirm/email/', EmailConfirmView.as_view())
]
