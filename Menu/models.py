import json
from django.db import models

class CategoriaMenu(models.Model):
    nombreCate = models.CharField(max_length=15)

    def __str__(self):
        return self.nombreCate

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    sabores = models.JSONField(blank=True, null=True, max_length=255)    
    precio = models.DecimalField(max_digits=10, decimal_places=2)   
    categoria = models.ForeignKey(CategoriaMenu, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre    
    
    def save(self, *args, **kwargs):
        # Si sabores es una cadena, divídela por comas y almacénala como una lista
        if isinstance(self.sabores, str):
            self.sabores = [sabor.strip() for sabor in self.sabores.split(',')]
        print (self.sabores)
        super().save(*args, **kwargs)