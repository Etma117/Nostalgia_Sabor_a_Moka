from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
from django.db import models
import os

from .models import Producto

@receiver(pre_delete, sender=Producto)
def eliminar_imagen_producto(sender, instance, **kwargs):
    # Eliminar la imagen asociada al producto cuando el producto se elimina
    if instance.imagen:
        ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(instance.imagen))
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)
