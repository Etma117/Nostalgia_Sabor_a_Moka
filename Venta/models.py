from django.db import models
from Comanda.models import Carrito


class Venta(models.Model):
    carrito = models.OneToOneField(Carrito, on_delete=models.CASCADE, null=True, blank=True, default=None)
    fecha_venta = models.DateField()
    hora_venta = models.TimeField()
