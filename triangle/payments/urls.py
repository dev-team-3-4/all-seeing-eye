from .views import *
from django.urls import path

urlpatterns = [
    path('input/', InputView.as_view(), name='buy_coins'),
    path('output/', OutputView.as_view(), name='send_coins'),
]
