from django.db import models
from .utils import upload_to_imagen, validar_tamanio_archivo, upload_to_fichero,upload_to_video, validate_image_quality
from functools import partial
from django.core.exceptions import ValidationError
from .errors import TamanioArchivoExcedidoError
from core.models import BaseModel
import os
from django.db.models.deletion import ProtectedError

from embed_video.fields import EmbedVideoField

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ImageSpecField
from .utils import validar_tamanio_archivo, delete_file






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


class Video(BaseModel):
    titulo = models.CharField(max_length=100, blank=True)
    archivo = EmbedVideoField(
        help_text="URL de YouTube o Vimeo",
    )
    tipo = models.CharField(max_length=50, choices=TIPOS_ARCHIVO, default='video', editable=False)

    objects = MediaManager()

    def __str__(self):
        return self.titulo











class Fichero(BaseModel):
    archivo = models.FileField(
        upload_to=upload_to_fichero,
        help_text="Extensiones permitidas: .pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx",
        null=True,
        blank=True,
        default=None
    )
    tipo = models.CharField(max_length=50, choices=TIPOS_ARCHIVO, default='fichero', editable=False)

    objects = MediaManager()

    def delete(self, *args, **kwargs):
        try:
            super().delete(*args, **kwargs)
        except ProtectedError:
            # El fichero está relacionado con otros elementos de la aplicación
            # Puedes realizar aquí la lógica que desees, como generar un mensaje de error o realizar alguna acción alternativa
            pass
        else:
            # El fichero se ha eliminado exitosamente
            # Aquí puedes realizar cualquier otra acción después de eliminar el fichero, como eliminar el archivo asociado
            delete_file(self.archivo)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        try:
            validar_tamanio_archivo(self.archivo)
        except TamanioArchivoExcedidoError as e:
            raise ValidationError(str(e))

    def __str__(self):
        return os.path.basename(self.archivo.name)







class Imagen(BaseModel):
    titulo = models.CharField(max_length=100, blank=True)
    archivo = models.ImageField(
        upload_to=upload_to_imagen,
        help_text="Extensiones permitidas: .jpg, .jpeg, .png, .gif, .bmp, .svg",
        default=None
    )
    tipo = models.CharField(max_length=50, choices=TIPOS_ARCHIVO, default='imagen', editable=False)

    small_thumbnail = ImageSpecField(
        source='archivo',
        processors=[ResizeToFill(350, 350)],
        format='JPEG',
        options={'quality': 70}
    )

    medium_thumbnail = ImageSpecField(
        source='archivo',
        processors=[ResizeToFit(800, 800)],
        format='JPEG',
        options={'quality': 70}
    )

    large_thumbnail = ImageSpecField(
        source='archivo',
        processors=[ResizeToFit(1600, 1600)],
        format='JPEG',
        options={'quality': 70}
    )
    objects = MediaManager()

    def delete(self, *args, **kwargs):
        try:
            super().delete(*args, **kwargs)
        except ProtectedError:
            # La imagen está relacionada con otros elementos de la aplicación
            # Puedes realizar aquí la lógica que desees, como generar un mensaje de error o realizar alguna acción alternativa
            pass
        else:
            # La imagen se ha eliminado exitosamente
            # Aquí puedes realizar cualquier otra acción después de eliminar la imagen, como eliminar el archivo asociado
            delete_file(self.archivo)

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


