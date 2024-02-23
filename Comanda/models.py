from django.db import models
from Menu.models import Producto
from django.contrib.auth.models import User

# Create your models here.
class Carrito(models.Model):
<<<<<<< HEAD
    items = models.ManyToManyField(Producto, through='CarritoItem')

    def __str__(self):
        return f"Carrito {self.id}"
=======
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    items = models.ManyToManyField(Producto, through='CarritoItem')

>>>>>>> e4e796027b5578c93ccdb4fcc368d9ec7b9c18d9
    
class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sabor = models.CharField(max_length=100, blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=0)