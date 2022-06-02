from django.db.models import *
from chats.models import Message

__all__ = ["SmartContract", "ModeratorInvite", "WithdrawalFundsRequest"]


class SmartContract(Model):
    first_user = ForeignKey("users.User", CASCADE, "first_contracts")
    second_user = ForeignKey("users.User", CASCADE, "second_contracts")
    moderator = ForeignKey("users.User", SET_NULL, "moderator_contracts",
                           default=None, null=True)
    chat = ForeignKey("chats.Chat", CASCADE, related_name="contracts")
    create_time = DateTimeField(auto_now_add=True)
    is_closed = BooleanField(default=False)
    bank = DecimalField(max_digits=10, decimal_places=2, default=0)


class ModeratorInvite(Message):
    smart_contract = ForeignKey("SmartContract", CASCADE, "moderator_invites")
    first_user_agree = BooleanField(default=False)
    second_user_agree = BooleanField(default=False)
    moderator = ForeignKey("users.User", CASCADE, "moderator_invites")


class WithdrawalFundsRequest(Message):
    smart_contract = ForeignKey("SmartContract", CASCADE, "withdrawal_requests")

    first_user_agree = BooleanField(default=False)
    second_user_agree = BooleanField(default=False)
    moderator_agree = BooleanField(default=False)

    first_user_funds = DecimalField(max_digits=10, decimal_places=2, default=0)
    second_user_funds = DecimalField(max_digits=10, decimal_places=2, default=0)
    moderator_funds = DecimalField(max_digits=10, decimal_places=2, default=0)

    close_contract = BooleanField(default=False)
