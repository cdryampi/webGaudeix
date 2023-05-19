import os
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import Imagen

@receiver(pre_delete, sender=Imagen)
def eliminar_archivo(sender, instance, **kwargs):
    # Obtener la ruta del archivo
    ruta_archivo = instance.archivo.path
    if os.path.isfile(ruta_archivo):
        # Eliminar el archivo del sistema de archivos
        os.remove(ruta_archivo)

@receiver(pre_save, sender=Imagen)
def eliminar_archivo_anterior(sender, instance, **kwargs):
    if instance.pk:
        # Si se está actualizando un objeto existente
        try:
            imagen_anterior = sender.objects.get(pk=instance.pk).archivo
        except sender.DoesNotExist:
            return

        nueva_imagen = instance.archivo
        if imagen_anterior and imagen_anterior != nueva_imagen:
            # Eliminar el archivo anterior
            ruta_archivo_anterior = imagen_anterior.path
            if os.path.isfile(ruta_archivo_anterior):
                os.remove(ruta_archivo_anterior)