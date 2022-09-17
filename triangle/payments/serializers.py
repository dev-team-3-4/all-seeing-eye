from rest_framework.serializers import *
from .models import *


__all__ = ['InputSerializer', 'OutputSerializer']


class OutputSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['coins_amount', 'blockchain_address']


class InputSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['hash']
