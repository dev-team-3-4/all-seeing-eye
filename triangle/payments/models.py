from django.db.models import *

__all__ = ['Transaction']


class Transaction(Model):
    class TYPES(TextChoices):
        OUTPUT = 'O', 'Output'
        INPUT = 'I', 'Input'

    user = ForeignKey('users.User', on_delete=SET_NULL, null=True)
    type = CharField(max_length=1, choices=TYPES.choices)
    wallet_amount = BigIntegerField()
    coins_amount = BigIntegerField()
    perform_time = DateTimeField(auto_now_add=True)
    blockchain_address = CharField(max_length=128)
    hash = CharField(max_length=128, unique=True)
