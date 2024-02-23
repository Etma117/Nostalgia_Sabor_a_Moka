from django.db import models
from Menu.models import Producto

# Create your models here.
class Carrito(models.Model):
    items = models.ManyToManyField(Producto, through='CarritoItem')

    def __str__(self):
        return f"Carrito {self.id}"
    
class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)