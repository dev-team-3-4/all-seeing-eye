from django.contrib import admin
from .models import *


@admin.register(SmartContract)
class SmartContractAdmin(admin.ModelAdmin):
    pass


@admin.register(ModeratorInvite)
class ModeratorInviteAdmin(admin.ModelAdmin):
    pass


@admin.register(WithdrawalFundsRequest)
class WithdrawalFundsRequestAdmin(admin.ModelAdmin):
    pass
