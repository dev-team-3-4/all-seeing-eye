from .views import *
from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('', UserViewSet.as_view(), name='registry'),
    path('me/', UserMeView.as_view(), name='me'),
    path('token/', ObtainAuthToken.as_view(), name='get token'),
    path('change/email/', EmailConfirmView.as_view(), name='change mail'),
    path('contacts/', UserContactViewSet.as_view(), name='contact set'),
    path('<str:username>/', UserView.as_view(), name='user'),
    path('<str:username>/contact/', UserContactView.as_view(), name='contact'),
    path('<str:username>/reset/', PasswordResetView.as_view(), name='reset password'),
    path('<str:username>/change/password/', ChangePasswordView.as_view(), name='change password'),
]
