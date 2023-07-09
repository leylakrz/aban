from django.contrib import admin

from .models import *


@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "current_price"]