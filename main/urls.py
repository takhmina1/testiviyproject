# from django.urls import path
# from . import views

# urlpatterns = [
#     path('create-transaction/', views.create_transaction, name='create_transaction'),
#     path('transactions/', views.get_transactions, name='get_transactions'),
# ]



from django.urls import path
from .views import UpdateRatesView

urlpatterns = [
    path('update-rates/', UpdateRatesView.as_view(), name='update_rates'),
]
