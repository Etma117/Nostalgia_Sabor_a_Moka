from django.urls import path
from .views import Pagar

urlpatterns = [
    path('pagar/', Pagar.as_view(), name='pagar'),
]
