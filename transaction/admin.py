from django.contrib import admin

from .models import *


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'user', 'cryptocurrency', 'number', 'total_price', 'status']

    def has_add_permission(self, request):
        return False
