from django.db.models import *

from bases.exceptions import APIException
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
    first_user_agree = BooleanField(default=None, null=True)
    second_user_agree = BooleanField(default=None, null=True)
    moderator = ForeignKey("users.User", CASCADE, "moderator_invites")
    checked = BooleanField(default=False)

    @property
    def is_agreed(self):
        if self.first_user_agree is None or self.second_user_agree is None:
            return None
        else:
            return self.first_user_agree and self.second_user_agree


class WithdrawalFundsRequest(Message):
    smart_contract = ForeignKey("SmartContract", CASCADE, "withdrawal_requests")

    first_user_agree = BooleanField(default=None, null=True)
    second_user_agree = BooleanField(default=None, null=True)
    moderator_agree = BooleanField(default=None, null=True)

    first_user_funds = DecimalField(max_digits=10, decimal_places=2, default=0)
    second_user_funds = DecimalField(max_digits=10, decimal_places=2, default=0)
    moderator_funds = DecimalField(max_digits=10, decimal_places=2, default=0)

    close_contract = BooleanField(default=False)

    @property
    def is_agreed(self):
        agree, not_def = 0, 0
        agree_list = [self.first_user_agree,
                      self.second_user_agree,
                      self.moderator_agree if self.smart_contract.moderator is not None else False]
        for value in agree_list:
            if value:
                agree += 1
            elif value is None:
                not_def += 1

        if agree >= 2:
            return True
        elif not_def > 0:
            return None
        else:
            return False

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_agreed:
            contract = self.smart_contract
            if contract.bank < self.first_user_funds + self.second_user_funds + self.moderator_funds:
                raise APIException("Not enough coins in contracts bank.", 403)
            if self.first_user_funds > 0:
                contract.first_user.coins += self.first_user_funds
                contract.bank -= self.first_user_funds
                contract.first_user.save()
            if self.second_user_funds > 0:
                contract.second_user.coins += self.second_user_funds
                contract.bank -= self.second_user_funds
                contract.second_user.save()
            if self.moderator_funds > 0:
                contract.moderator.coins += self.moderator_funds
                contract.bank -= self.moderator_funds
                contract.moderator.save()

            contract.is_closed = self.close_contract
            contract.save()

        super(WithdrawalFundsRequest, self).save(force_insert, force_update, using, update_fields)
