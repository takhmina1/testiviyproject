# from asgiref.sync import sync_to_async
# import httpx
# import asyncio
# from django.conf import settings
# from .models import Currency

# async def check_coingecko_api():
#     url = "https://api.coingecko.com/api/v3/simple/price"
#     params = {
#         'ids': 'bitcoin,ethereum',
#         'vs_currencies': 'usd'
#     }
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, params=params)
#         response.raise_for_status()
#         data = response.json()
#         return data

# # @sync_to_async
# # def update_crypto_rates_in_database(data):
# #     for Currency_code, info in data.items():
# #         rate_to_usd = info['usd']
# #         Currency.objects.update_or_create(
# #             code=Currency_code.upper(),
# #             defaults={'rate_to_usd': rate_to_usd}
# #         )



# async def update_crypto_rates():
#     data = await check_coingecko_api()
#     await update_crypto_rates_in_database(data)

# async def fetch_fiat_data_from_api():
#     url = "https://data.fx.kg/api/v1/currencies"
#     headers = {
#         'Authorization': 'Bearer xrQq7XzYLGGXvK2ci0X9jhUKRJMvxnFBS9GiLnMAffb77394'
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         return data






# @sync_to_async
# def update_crypto_rates_in_database(data):
#     for Currency_code, info in data.items():
#         rate_to_usd = info['usd']
#         Currency.objects.update_or_create(
#             code=Currency_code.upper(),
#             defaults={'rate_to_usd': rate_to_usd}
#         )








# @sync_to_async
# def update_fiat_rates_in_database(data):
#     for Currency in data['data']:
#         code = Currency['code']
#         rate_to_usd = Currency['rate_to_usd']
#         Currency.objects.update_or_create(
#             code=code,
#             defaults={'rate_to_usd': rate_to_usd}
#         )

# async def update_fiat_rates():
#     data = await fetch_fiat_data_from_api()
#     await update_fiat_rates_in_database(data)

# async def main():
#     await update_crypto_rates()
#     await update_fiat_rates()

# asyncio.run(main())










import httpx
import asyncio
from asgiref.sync import sync_to_async
from .models import Currency

async def check_coingecko_api():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin,ethereum',
        'vs_currencies': 'usd'
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

async def fetch_fiat_data_from_api():
    url = "https://data.fx.kg/api/v1/currencies"
    headers = {
        'Authorization': 'Bearer xrQq7XzYLGGXvK2ci0X9jhUKRJMvxnFBS9GiLnMAffb77394'
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@sync_to_async
def update_crypto_rates_in_database(data):
    for currency_code, info in data.items():
        rate_to_usd = info['usd']
        Currency.objects.update_or_create(
            code=currency_code.upper(),
            defaults={'rate_to_usd': rate_to_usd}
        )

@sync_to_async
def update_fiat_rates_in_database(data):
    for currency in data['data']:
        code = currency['code']
        rate_to_usd = currency['rate_to_usd']
        Currency.objects.update_or_create(
            code=code,
            defaults={'rate_to_usd': rate_to_usd}
        )

async def update_crypto_rates():
    data = await check_coingecko_api()
    await update_crypto_rates_in_database(data)

async def update_fiat_rates():
    data = await fetch_fiat_data_from_api()
    await update_fiat_rates_in_database(data)

async def main():
    await update_crypto_rates()
    await update_fiat_rates()
