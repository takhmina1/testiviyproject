from rest_framework import serializers
from .models import Currency, Wallet, ExchangeRate, TransactionFee, ExchangeTransaction
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'rate_to_usd']

class WalletSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'currency', 'balance']

class ExchangeRateSerializer(serializers.ModelSerializer):
    from_currency = CurrencySerializer()
    to_currency = CurrencySerializer()

    class Meta:
        model = ExchangeRate
        fields = ['id', 'from_currency', 'to_currency', 'rate', 'updated_at']

class TransactionFeeSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = TransactionFee
        fields = ['id', 'currency', 'fee_percentage']

class ExchangeTransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    from_wallet = WalletSerializer()
    to_wallet = WalletSerializer()
    exchange_rate = ExchangeRateSerializer()

    class Meta:
        model = ExchangeTransaction
        fields = ['id', 'user', 'from_wallet', 'to_wallet', 'amount_from', 'amount_to', 'exchange_rate', 'created_at', 'status', 'fee']
