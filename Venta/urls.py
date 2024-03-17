from django.urls import path
from .views import Ventas

urlpatterns = [
    path('pagar/', Ventas, name='pagar'),
]