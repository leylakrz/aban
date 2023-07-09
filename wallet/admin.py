from django.contrib import admin

from wallet.models import Wallet, WalletCryptocurrency


class WalletCryptocurrencyInline(admin.TabularInline):
    model = WalletCryptocurrency

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["user"]
    inlines = [WalletCryptocurrencyInline]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

