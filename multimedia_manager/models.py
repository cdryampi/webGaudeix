from django.db import models
from .utils import upload_to_imagen, validar_tamanio_archivo
from functools import partial
from django.core.exceptions import ValidationError
from .errors import TamanioArchivoExcedidoError
import os


TIPOS_ARCHIVO = (
    ('imagen', 'Imagen'),
    ('video', 'Video'),
    ('fichero', 'Fichero'),
)


class MediaManager(models.Manager):
    def images(self):
        return self.filter(tipo='imagen')

    def videos(self):
        return self.filter(tipo='video')

    def pdfs(self):
        return self.filter(tipo='fichero')



class Imagen(models.Model):
    titulo = models.CharField(max_length=100, blank=True)
    archivo = models.ImageField(
        upload_to=upload_to_imagen,
        help_text="Extensiones permitidas: .jpg, .jpeg, .png, .gif, .bmp, .svg",
        null=True,
        blank=True,
        default=None
    )
    tipo = models.CharField(max_length=50, choices=TIPOS_ARCHIVO, default='imagen', editable=False)

    objects = MediaManager()

    def save(self, *args, **kwargs):
        if not self.id:
            # Obtener el nombre original sin extensión
            nombre_original = os.path.splitext(self.archivo.name)[0]
            self.titulo = nombre_original
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        try:
            validar_tamanio_archivo(self.archivo)
        except TamanioArchivoExcedidoError as e:
            raise ValidationError(str(e))
    def __str__(self) -> str:
        return self.titulo
        


