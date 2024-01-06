import json
from django.db import models

class CategoriaMenu(models.Model):
    nombreCate = models.CharField(max_length=15)

    def __str__(self):
        return self.nombreCate

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    sabores = models.JSONField(blank=True, null=True)    
    precio = models.DecimalField(max_digits=10, decimal_places=2)   
    categoria = models.ForeignKey(CategoriaMenu, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre    