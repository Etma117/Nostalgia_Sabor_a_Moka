from django.db import models
from Menu.models import Producto
from django.contrib.auth.models import User

# Create your models here.
class Mesa(models.Model):
    numero = models.IntegerField(unique=True)

class PedidoDomicilio(models.Model):
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    mesa = models.ForeignKey(Mesa , on_delete=models.CASCADE, null=True, blank=True)
    pedido_domicilio = models.ForeignKey(PedidoDomicilio, on_delete=models.CASCADE, null=True, blank=True)
    # items = models.ManyToManyField(Producto, through='CarritoItem')
    
class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sabor = models.CharField(max_length=100, blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=0)