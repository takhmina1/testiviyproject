from django.contrib import admin
from .models import Currency, Wallet, ExchangeRate, TransactionFee, ExchangeTransaction

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'rate_to_usd']

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'currency', 'balance']

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['from_currency', 'to_currency', 'rate', 'updated_at']

@admin.register(TransactionFee)
class TransactionFeeAdmin(admin.ModelAdmin):
    list_display = ['currency', 'fee_percentage']

@admin.register(ExchangeTransaction)
class ExchangeTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'from_wallet', 'to_wallet', 'amount_from', 'amount_to', 'exchange_rate', 'created_at', 'status', 'fee']
