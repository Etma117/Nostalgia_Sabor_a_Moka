from django.urls import path
from .views import Ventas

urlpatterns = [
    path('ventas/', Ventas, name='pagar'),
]