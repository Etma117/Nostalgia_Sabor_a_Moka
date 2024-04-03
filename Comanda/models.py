from django.db import models
from Menu.models import Producto, Adicional

# Create your models here.
class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    def __str__(self):
        return f"Mesa {self.numero}"

class PedidoDomicilio(models.Model):
    nombre = models.CharField(max_length=200, null=True, blank=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)

class Carrito(models.Model):
    mesa = models.ForeignKey(Mesa , on_delete=models.CASCADE, null=True, blank=True)
    pedido_domicilio = models.ForeignKey(PedidoDomicilio, on_delete=models.CASCADE, null=True, blank=True)
    items = models.ManyToManyField(Producto, through='CarritoItem')

    def obtener_total(self):
        return sum(item.subtotal for item in self.carritoitem_set.all())

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sabor = models.CharField(max_length=100, blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=0)
    comentario= models.CharField(max_length=500, blank= True, null=True)
    adicional = models.ForeignKey(Adicional, on_delete=models.SET_NULL, blank=True, null=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    def calcular_subtotal(self):
        subtotal = self.producto.precio * self.cantidad
        if self.adicional:
            subtotal += self.adicional.precio_extra * self.cantidad
        return subtotal

    def save(self, *args, **kwargs):
        self.subtotal = self.calcular_subtotal()
        super().save(*args, **kwargs)