from django.contrib import admin
from .models import *


@admin.register(Chat)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class EmailConfirmObjectAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatMember)
class PasswordResetObjectAdmin(admin.ModelAdmin):
    pass

