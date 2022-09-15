from django.contrib import admin
from .models import *


@admin.register(Transaction)
class Transaction(admin.ModelAdmin):
    pass
