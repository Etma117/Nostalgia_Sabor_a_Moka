import json
from django.db import models

from django.db import models

class CategoriaMenu(models.Model):
    nombreCate = models.CharField(max_length=15)

    def __str__(self):
        return self.nombreCate

class Adicional(models.Model):
   
    nombre = models.CharField(max_length=50)
    precio_extra = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    sabores_raw = models.CharField(max_length=255, blank=True, null=True) 
    precio = models.DecimalField(max_digits=10, decimal_places=2)   
    categoria = models.ForeignKey(CategoriaMenu, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    adicionales = models.ManyToManyField('Adicional', related_name='ingredientes_adicionales', blank=True)

    def obtener_sabores(self):
        if self.sabores_raw:
            return [sabor.strip() for sabor in self.sabores_raw.split(',')]
        else:
            return ['Ninguno']

    def set_sabores(self, sabores):
        self.sabores_raw = ', '.join(sabores)

    sabores = property(obtener_sabores, set_sabores)

    def __str__(self):
        return self.nombre
 
    
