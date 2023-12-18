from django.db import models

class Sabor(models.Model):
    TIPO_CHOICES = [
        ('alitas', 'Alitas'),
        ('cafe', 'Café'),
        # Agrega más tipos según sea necesario
    ]

    nombre = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
    
class Categoria(models.Model):
    nombreCate = models.CharField(max_length=15)

    def __str__(self):
        return self.nombreCate

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    sabores = models.ManyToManyField(Sabor, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)

    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre