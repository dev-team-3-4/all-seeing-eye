from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailConfirmObject)
class EmailConfirmObjectAdmin(admin.ModelAdmin):
    pass


@admin.register(PasswordResetObject)
class PasswordResetObjectAdmin(admin.ModelAdmin):
    pass

