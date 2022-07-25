from django.contrib import admin
from .models import *


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatMember)
class ChatMemberAdmin(admin.ModelAdmin):
    pass

