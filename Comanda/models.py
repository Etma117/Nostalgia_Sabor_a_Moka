from django.db import models
from Menu.models import Producto
from django.contrib.auth.models import User

# Create your models here.
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    items = models.ManyToManyField(Producto, through='CarritoItem')

    
class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sabor = models.CharField(max_length=100, blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=0)