from django.db import models
from .utils import upload_to_imagen, validar_tamanio_archivo, upload_to_fichero,upload_to_video, validate_image_quality, upload_to_audio
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
from personalizacion.utils import get_parallax_image_path, get_carrousel_image_path





TIPOS_ARCHIVO = (
    ('imagen', 'Imagen'),
    ('video', 'Video'),
    ('fichero', 'Fichero'),
    ('audio', 'Audio'),
)


class MediaManager(models.Manager):
    def images(self):
        return self.filter(tipo='imagen')

    def videos(self):
        return self.filter(tipo='video')

    def pdfs(self):
        return self.filter(tipo='fichero')
    
    def audios(self):
        return self.filter(tipo='audio')


class Video(BaseModel):
    titulo = models.CharField(max_length=100, blank=True)
    archivo = models.FileField(
        upload_to=upload_to_video,
        help_text="Extensiones permitidas: .mp4, .avi, .mov, .mkv",
        null=True,
        blank=True,
        default=None
    )
    tipo = models.CharField(max_length=50, choices=TIPOS_ARCHIVO, default='video', editable=False)

    objects = MediaManager()

    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = 'Vídeo'
        verbose_name_plural = 'vídeos'











class Fichero(BaseModel):
    titulo = models.CharField(max_length=100, blank=True)
    archivo = models.FileField(
        upload_to=upload_to_fichero,
        help_text="Extensiones permitidas: .pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx, .zip",
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
        return self.titulo
    class Meta:
        verbose_name = 'Fitxer'
        verbose_name_plural = 'Fitxers'







class Imagen(BaseModel):
    titulo = models.CharField(max_length=100, blank=True)
    archivo = models.ImageField(
        upload_to=upload_to_imagen,
        help_text="Extensiones permitidas: .jpg, .jpeg, .png, .gif, .bmp, .svg, webp",
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

    def clean(self):
        super().clean()
        try:
            validar_tamanio_archivo(self.archivo)
        except TamanioArchivoExcedidoError as e:
            raise ValidationError(str(e))
        

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Imatge'
        verbose_name_plural = 'Imatges'





class Parallax(models.Model):
    
    titulo = models.CharField(
        max_length=100,
        verbose_name="Títol"
    )
    descripcion_corta = models.CharField(
        max_length=200,
        null= True,
        blank= True,
        verbose_name="Descripció curta"
    )
    imagen = models.ImageField(
        upload_to=get_parallax_image_path,
        verbose_name="Imatge"
    )
    publicado = models.BooleanField(
        default=False,
        verbose_name="Publicat"
    )

    def __str__(self):
        return self.titulo



class VideosEmbed(models.Model):
    """
        Clase que representa a un EmbedVideo
    """
    titulo = models.CharField(
        max_length=100,
        help_text="Títol del Vídeo.",
        verbose_name="Títola"
    )
    publicado = models.BooleanField(
        default=False,
        verbose_name="Publicat"
    )
    video = models.OneToOneField(Video, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"Portada de video: {self.titulo}"
    


class Audio(BaseModel):
    """
        Clase que representa a un Audio
    """
    titulo = models.CharField(max_length=100, blank=True)
    
    archivo = models.FileField(
        upload_to=upload_to_audio,
        help_text="Extensiones permitidas: .mp3, .wav, etc.",  # Especifica las extensiones permitidas
        null=True,
        blank=True,
        default=None
    )
    
    tipo = models.CharField(max_length=50, choices=TIPOS_ARCHIVO, default='audio', editable=False)

    objects = MediaManager()

    def delete(self, *args, **kwargs):
        try:
            super().delete(*args, **kwargs)
        except ProtectedError:
            # El fichero está relacionado con otros elementos de la aplicación
            # Puedes realizar aquí la lógica que deeses, como generar un mensaje de error o realizar alguna acción alternativa
            pass
        else:
            # El fichero se ha eliminado exitosamente
            # Aquí puedes realizar cualquier otra acción después de eliminar el fichero, como eliminar el archivo asociado
            delete_file(self.archivo)

    def clean(self):
        super().clean()
        try:
            validar_tamanio_archivo(self.archivo)
        except TamanioArchivoExcedidoError as e:
            raise ValidationError(str(e))
    
    def __str__(self):
           return self.titulo

    class Meta:
       verbose_name = 'Àudio'
       verbose_name_plural = 'Àudios'


class Carrusel(models.Model):
    """
        Modelo que representa a un carrusel
    """
    TIPO_OPCIONES = (
    ('carrusel', 'Carrusel'),
    ('collage', 'Collage'),
    )
    titulo = models.CharField(
        max_length=100,
        verbose_name="Títol del Carrusel intern"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripció intern"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Actiu"
    )
    tipo = models.CharField(
    max_length=8,
    choices=TIPO_OPCIONES,
    default='carrusel',
    verbose_name="Tipus de visualització"
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Carrusel'
        verbose_name_plural = 'Carrusels'

class ImagenCarrusel(models.Model):
    carrusel = models.ForeignKey(
        Carrusel,
        related_name='imatges',
        verbose_name="Carrusel",
        on_delete=models.CASCADE
    )
    imagen = models.ImageField(
        upload_to=get_carrousel_image_path,
        validators=[validar_tamanio_archivo],
        verbose_name="Imatge"
    )
    small_thumbnail = ImageSpecField(
        source='imagen',
        processors=[ResizeToFill(350, 350)],
        format='JPEG',
        options={'quality': 70}
    )

    medium_thumbnail = ImageSpecField(
        source='imagen',
        processors=[ResizeToFit(800, 800)],
        format='JPEG',
        options={'quality': 70}
    )

    large_thumbnail = ImageSpecField(
        source='imagen',
        processors=[ResizeToFit(1600, 1600)],
        format='JPEG',
        options={'quality': 70}
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Caption",
        help_text= "Descripció per l'imatge que sortirà a la web."
    )
    orden = models.PositiveIntegerField(
        default=0,
        help_text="Defineix l'ordre de la imatge en el carrusel",
        verbose_name="Ordre"
    )

    def __str__(self):
        return f"Imatge {self.id} del {self.carrusel.titulo}"

    class Meta:
        ordering = ['orden']
        verbose_name = 'Imatge del Carrusel'
        verbose_name_plural = 'Imatges del Carrusel'