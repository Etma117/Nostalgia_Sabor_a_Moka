from django.db import models
from Comanda.models import Mesa
from Menu.models import Producto

class Venta(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, blank=True, null=True)
    pedido_domicilio=models.CharField(max_length=300, blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class VentaItem(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalle')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    sabor = models.CharField(max_length=100, blank=True, null=True)
    adicionales = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} - Subtotal: {self.subtotal}"
