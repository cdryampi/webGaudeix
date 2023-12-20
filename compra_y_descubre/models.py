from django.db import models
from multimedia_manager.models import Fichero, Imagen
from django.utils import timezone
from django.urls import reverse
from blog.models import Tag
from map.models import MapPoint
from agenda.models import Agenda
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from colorfield.fields import ColorField
from core.models import BaseModel, MetadataModel

from django.conf import settings
from gaudeix.settings import DOMAIN_URL
#RQ
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.core.files.base import ContentFile



# Create your models here.
class EntidadComprayParticipa(models.Model):
    """
        modelo que representa una entidad que participa en 'Compra y participa'
    """
    
    nombre = models.CharField(
        max_length=255,
        help_text="Títol per l'entitat compra i descobreix. PE: La mer",
        verbose_name="Títol"
    )
    enllace = models.URLField(
        blank=True,
        help_text="Afegeix el link de la fitxa per l'entitat ",
        verbose_name="Comerciant"
    )
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Entitat"
        verbose_name_plural = "Entitats"



class CompraDescubre(BaseModel, MetadataModel):
    """
        modelo que representa una entidad compra y descubre pensada para las campañas de 'xarxabarris.cat' .
    """
    titulo = models.CharField(
        max_length=255,
        help_text="Títol pel compra i descobreix. PE: Compra i descobreix 2023",
        verbose_name="Títol"
    )
    slug = models.SlugField(
        unique=True,
        editable=False,
        help_text="Slug automàtic generat a partir del títol",
    )
    primary_color = ColorField(
        default='#FFFFFF',
        verbose_name="Color primari"
    )
    secondary_color = ColorField(
        default='#FFFFFF',
        verbose_name="Color secondary"
    )
    fecha_inicio = models.DateField(
        default=timezone.now,
        help_text="Data de l'esdeveniment Compra i descobreix",
        verbose_name="Data de l'esdeveniment"
    )
    fecha_fin = models.DateField(
        default=timezone.now,
        help_text="Data de finalització de l'esdeveniment Compra i descobreix",
        verbose_name="Data de finalització"
    )
    publicado = models.BooleanField(
        default=False,
        help_text="Indica si l'esdeveniment especial està publicat",
        verbose_name="Publicat"
    )

    descripcion_larga = RichTextField(
        help_text="Descripció llarga de l'esdeveniment Compra i descobreix",
        null=True,
        blank=True,
        verbose_name="Descripció llarga"
    )
    descripcion_corta = RichTextField(
        help_text="Descripció curta de l'esdeveniment Compra i descobreix",
        null=True,
        blank=True,
        verbose_name="Descripció curta"
    )
    entidades = models.ManyToManyField(
        EntidadComprayParticipa,
        blank=True,
        help_text="Selecciona tots els comerços vinculats amb l'event Compra i descobreix",
        verbose_name="Comerços Compra i descobreix"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="Tags"
    )
    participante = models.URLField(
        blank=True,
        help_text="Afegeix el link per els participants",
        verbose_name="Participant"
    )
    comerciante = models.URLField(
        blank=True,
        help_text="Afegeix el link per els comerciants",
        verbose_name="Comerciant"
    )
    sorteo = models.URLField(
        blank=True,
        help_text="Afegeix el link del sorteig",
        verbose_name= "sorteix"
    )

    qr_code = models.ImageField(
        upload_to='qr_codes/',  # Directorio donde se guardarán los códigos QR
        null=True,
        blank=True,
        verbose_name="Codi QR"
    )
    
    def save(self, *args, **kwargs):
        if not self.slug or not self.id:
            self.slug = slugify(self.titulo)

            # Regenera el código QR y guarda los datos binarios en el campo qr_code
            qr = qrcode.QRCode(
                version=10,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2,
            )
            qr.add_data(f'{DOMAIN_URL}{self.get_absolute_url()}')
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Crear un offset para centrar el código QR en una imagen de 310x310
            qr_offset = Image.new('RGB', (750, 750), 'white')
            qr_offset.paste(qr_image, (75, 75))
            
            # Guardar la imagen en un flujo de bytes en formato PNG
            stream = BytesIO()
            qr_offset.save(stream, 'PNG')
            
            # Crear un archivo ContentFile a partir de los datos binarios del flujo de bytes
            file_name = f'{self.titulo}-{self.id}-qr.png'
            content_file = ContentFile(stream.getvalue(), name=file_name)
            
            # Asignar el archivo al campo qr_code
            self.qr_code.save(file_name, content_file, save=False)

        else:
            # Verificar si el slug ya existe y el objeto ya existe
            if CompraDescubre.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                # Generar un slug único basado en la fecha y hora actual
                timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
                self.slug = f"{self.slug}-{timestamp}"
            
                        # Regenera el código QR y guarda los datos binarios en el campo qr_code
            if self.qr_code:
                self.qr_code.delete()
            
            qr = qrcode.QRCode(
                version=10,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2,
            )
            qr.add_data(f'{DOMAIN_URL}{self.get_absolute_url()}')
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Crear un offset para centrar el código QR en una imagen de 310x310
            qr_offset = Image.new('RGB', (750, 750), 'white')
            qr_offset.paste(qr_image, (75, 75))
            
            # Guardar la imagen en un flujo de bytes en formato PNG
            stream = BytesIO()
            qr_offset.save(stream, 'PNG')
            
            # Crear un archivo ContentFile a partir de los datos binarios del flujo de bytes
            file_name = f'{self.titulo}-{self.id}-qr.png'
            content_file = ContentFile(stream.getvalue(), name=file_name)
            
            # Asignar el archivo al campo qr_code
            self.qr_code.save(file_name, content_file, save=False)

        super().save(*args, **kwargs)
    
    def is_now(self):
        """
        reporta si hemos superado el tiempo limite del evento
        """
        return self.fecha_inicio > timezone.now().date()
    
    def has_ended(self):
        """
        Retorna True si el evento ha terminado (ha pasado la fecha de finalización).
        """
        return self.fecha_fin < timezone.now().date()
    
    def get_absolute_url(self):
        return reverse('compra_y_descubre:compra_y_descubre', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Esdeveniment Especial 'Compra i descobreix'."
        verbose_name_plural = "Esdeveniments Especials 'Compra i descobreix'."





class CompraDescubrePasosImagen(models.Model):
    compradescubre = models.ForeignKey(
        CompraDescubre,
        on_delete=models.CASCADE,
        default=None
    )
    titulo = models.CharField(
        max_length=255,
        help_text="Títol pel compra i descobreix. PE: Pas 2A. Format paper",
        verbose_name="Títol"
    )
    descripcion = RichTextField(
        help_text="Descripció del pas l'esdeveniment Compra i descobreix",
        null=True,
        blank=True,
        verbose_name="Descripció curta"
    )
    imagen = models.ForeignKey(
        Imagen,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Post: {self.compradescubre.titulo} - Imatge: {self.imagen}"
    
    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = CompraDescubrePasosImagen.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)


class CompraDescubreGaleriaImagen(models.Model):
    compradescubre = models.ForeignKey(
        CompraDescubre,
        on_delete=models.CASCADE,
        default=None
    )
    imagen = models.ForeignKey(
        Imagen,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Post: {self.compradescubre.titulo} - Imatge: {self.imagen}"
    
    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = CompraDescubreGaleriaImagen.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Galeria dels guanyadors de l'esdeveniment 'compra i descobreix'."


class CompraDescubreImagen(models.Model):
    """
    Modelo para asociar una imagen a un CompraDescubre.
    """
    compradescubre = models.OneToOneField(
        CompraDescubre,
        on_delete=models.CASCADE, null=True,
        verbose_name="CompraDescubre"
    )
    imagen = models.OneToOneField(
        Imagen,
        on_delete=models.CASCADE,
        verbose_name="Imatge"
    )

    def __str__(self):
        return f"CompraDescubre: {self.compradescubre} - Imatge: {self.imagen}"

    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = CompraDescubreImagen.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)



class CompraDescubreFichero(models.Model):
    """
        modelo que representa un fichero PDF o siminar que sirva como instructivo para el evento de 'compra y descubre'
    """
    compradescubre = models.OneToOneField(
        CompraDescubre,
        on_delete=models.CASCADE,
        null=True
    )

    fichero = models.OneToOneField(
        Fichero,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Evento: {self.compradescubre} - Fichero: {self.fichero}"

    def delete(self, *args, **kwargs):
        # Eliminar la imagen asociada antes de eliminar el objeto SubBlogImagen
        # self.evento.delete() .-.
        self.fichero.delete()
        super().delete(*args, **kwargs)


