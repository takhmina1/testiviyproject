from django.db import models
from django.contrib.auth.models import User

# Модель для хранения информации о валютах
class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True)  # Уникальный код валюты (например, USD, BTC)
    name = models.CharField(max_length=50)              # Полное название валюты (например, "US Dollar", "Bitcoin")
    rate_to_usd = models.DecimalField(max_digits=20, decimal_places=10, default=0.0)  # Курс к USD

    def __str__(self):
        return self.name

# Модель для хранения информации о кошельках пользователей
class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, которому принадлежит кошелек
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)  # Валюта кошелька
    balance = models.DecimalField(max_digits=20, decimal_places=10, default=0.0)  # Баланс кошелька

    def __str__(self):
        return f"{self.user.username} - {self.currency.code} - {self.balance}"

# Модель для хранения информации о курсах обмена валют
class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Currency, related_name='from_currency', on_delete=models.CASCADE)
    to_currency = models.ForeignKey(Currency, related_name='to_currency', on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=20, decimal_places=10)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.from_currency} to {self.to_currency} - {self.rate}"

# Модель для хранения информации о комиссиях за транзакции
class TransactionFee(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)  # Валюта, для которой применяется комиссия
    fee_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Комиссия в процентах

    def __str__(self):
        return f"{self.currency.code} - {self.fee_percentage}%"

# Модель для хранения информации о транзакциях обмена валют
class ExchangeTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, совершающий транзакцию
    from_wallet = models.ForeignKey(Wallet, related_name='from_wallet', on_delete=models.CASCADE, null=True, blank=True)  # Кошелек отправителя (необязательный)
    to_wallet = models.ForeignKey(Wallet, related_name='to_wallet', on_delete=models.CASCADE, null=True, blank=True)  # Кошелек получателя (необязательный)
    amount_from = models.DecimalField(max_digits=20, decimal_places=10)  # Сумма отправки
    amount_to = models.DecimalField(max_digits=20, decimal_places=10)  # Сумма получения
    exchange_rate = models.ForeignKey(ExchangeRate, on_delete=models.CASCADE)  # Курс обмена
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания транзакции
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])  # Статус транзакции
    fee = models.DecimalField(max_digits=20, decimal_places=10, default=0.0)  # Комиссия за транзакцию

    def __str__(self):
        return f"Exchange {self.amount_from} {self.from_wallet.currency if self.from_wallet else 'N/A'} to {self.amount_to} {self.to_wallet.currency if self.to_wallet else 'N/A'} for user {self.user.username}"

    def calculate_fee(self):
        """ Рассчитывает комиссию за транзакцию """
        try:
            fee_percentage = TransactionFee.objects.get(currency=self.from_wallet.currency).fee_percentage
            self.fee = (self.amount_from * fee_percentage) / 100
        except TransactionFee.DoesNotExist:
            self.fee = 0.0

    def execute_transaction(self):
        """ Выполняет транзакцию, обновляет балансы кошельков и учитывает комиссию """
        self.calculate_fee()
        total_amount_from = self.amount_from + self.fee

        if self.from_wallet and self.to_wallet:
            if self.from_wallet.balance >= total_amount_from:
                self.from_wallet.balance -= total_amount_from
                self.to_wallet.balance += self.amount_to
                self.from_wallet.save()
                self.to_wallet.save()
                self.status = 'completed'
            else:
                self.status = 'failed'
        else:
            # Логика обработки транзакций без кошельков
            self.status = 'completed' if total_amount_from <= self.amount_from else 'failed'

        self.save()

# Функция для создания и выполнения транзакций
def create_and_execute_transaction(user, from_wallet_id, to_wallet_id, amount_from):
    from_wallet = Wallet.objects.get(id=from_wallet_id) if from_wallet_id else None
    to_wallet = Wallet.objects.get(id=to_wallet_id) if to_wallet_id else None
    if from_wallet and to_wallet:
        exchange_rate = ExchangeRate.objects.get(from_currency=from_wallet.currency, to_currency=to_wallet.currency)
        amount_to = amount_from / exchange_rate.rate
    else:
        exchange_rate = None
        amount_to = amount_from  # При отсутствии обмена используем прямую сумму

    transaction = ExchangeTransaction(
        user=user,
        from_wallet=from_wallet,
        to_wallet=to_wallet,
        amount_from=amount_from,
        amount_to=amount_to,
        exchange_rate=exchange_rate
    )
    transaction.execute_transaction()
    return transaction
