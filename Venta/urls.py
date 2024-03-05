from django.urls import path
from .views import Pagar, ventas

urlpatterns = [
    path('procesar_pago/', Pagar, name='procesar_pago'),
    path('Ventas/', ventas.as_view(), name='ventas')
]
