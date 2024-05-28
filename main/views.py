# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Wallet, ExchangeTransaction
# from .serializers import ExchangeTransactionSerializer

# @api_view(['POST'])
# def create_transaction(request):
#     """
#     Создание новой транзакции.
#     ---
#     parameters:
#       - name: user_id
#         description: ID пользователя, инициирующего транзакцию
#         required: true
#         type: integer
#         format: int64
#       - name: from_wallet_id
#         description: ID кошелька отправителя
#         required: true
#         type: integer
#         format: int64
#       - name: to_wallet_id
#         description: ID кошелька получателя
#         required: true
#         type: integer
#         format: int64
#       - name: amount_from
#         description: Сумма для отправки со счета отправителя
#         required: true
#         type: number
#         format: double
#     responses:
#       201:
#         description: Транзакция успешно создана
#         schema:
#           $ref: '#/definitions/ExchangeTransaction'
#       400:
#         description: Некорректный запрос, неверные параметры
#     """
#     serializer = ExchangeTransactionSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def get_transactions(request):
#     """
#     Получение всех транзакций.
#     ---
#     responses:
#       200:
#         description: Список всех транзакций
#         schema:
#           type: array
#           items:
#             $ref: '#/definitions/ExchangeTransaction'
#     """
#     transactions = ExchangeTransaction.objects.all()
#     serializer = ExchangeTransactionSerializer(transactions, many=True)
#     return Response(serializer.data)
    







from django.http import JsonResponse
from django.views import View
import asyncio
from .services import update_crypto_rates, update_fiat_rates

class UpdateRatesView(View):
    async def get(self, request, *args, **kwargs):
        await asyncio.gather(
            update_crypto_rates(),
            update_fiat_rates()
        )
        return JsonResponse({'status': 'success'})
