from django.db import models

from django.utils.text import slugify
from colorfield.fields import ColorField
from core.models import BaseModel, MetadataModel
from multimedia_manager.models import Fichero, Imagen, Parallax
from multimedia_manager.models import Video
from agenda.models import Agenda
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.urls import reverse
from blog.models import Tag, Categoria, Post

from django.conf import settings
from gaudeix.settings import DOMAIN_URL
#RQ
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.core.files.base import ContentFile

from decimal import Decimal


# Create your models here.


class Autor(models.Model):
    """
        Modelo que representa a un autor de un mensaje para el evento especial
    """

    nombre = models.CharField(
        max_length=100,
        verbose_name="Nom",
        help_text="Afegix el nom i cognom."
    )
    cargo = models.CharField(
        max_length=100,
        verbose_name="càrrec"
    )
    foto = models.ImageField(
        upload_to='autores/',
        blank=True,
        null=True,
        verbose_name="Imatge",
        help_text="Afegeix un foto per l'autor"
    )

    def __str__(self):
        return f"{self.nombre} ({self.cargo})"

    


class Mensaje(models.Model):
    """
        Modelo que representa a un mensaje de un usuario
    """

    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        verbose_name="Autor",
        help_text="Afegeix un Autor del comentari"
    )
    nombre_interno = models.CharField(
        max_length=255,
        verbose_name="Nom intern",
        help_text="Afegeix un nom intern per al missatge, per exemple: 'Missatge del Nadal 2023 de Sergi Teodoro'"
    )
    titulo = models.CharField(
        max_length=255,
        verbose_name="Títol",
        help_text="Afegeix el títol del missatge, per exemple: 'Dies de família, dies de poble' o 'Les entitats, pilar fonamental de Nadal'"
    )
    contenido = RichTextField(
        verbose_name="comentari",
        help_text="Afegeix un missatge per l'esdeveniment"
    )
    mensaje_despedida = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Missatge de comiat",
        help_text="Afegeix un missatge de comiat, per exemple: 'Bon Nadal' o 'Bon Nadal i feliç 2023!'"
    )


    def __str__(self):
        return f"{self.nombre_interno} - {self.titulo}"
    
    class Meta:
        verbose_name_plural = "Missatges de l'esdeveniment"
        verbose_name = "missatge"

class MedidaEconomica(models.Model):
    """
        Clase que representa una medida económica para los eventos especiales que representan el conjunto de las fiestas del pueblo.
    """
    titulo = models.CharField(
        max_length=200,
        verbose_name="Nom de la mesura",
        help_text="Afegeix el nom de la mesura ."
    )
    titulo_html = models.CharField(
        max_length=200,
        verbose_name="Títol de la mesura",
        help_text="Afegeix el títol de la mesura per la web."
    )
    descripcion = models.TextField(
        verbose_name="Descripció",
        help_text="Afegeix la descripció de la mesura econòmica per la web(sortirà el popup)."
    )
    impacto_economico = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Impacte Econòmic Estimat",
        help_text="Afegeix l'augment o l'estalvi de €."
    )
    publicado = models.BooleanField(
        default=False,
        verbose_name="Publicat",
        help_text="Marca si la mesura està disponible."
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Mesures Econòmica"
        verbose_name_plural = "Mesures Econòmiques"



class EventoEspecial(BaseModel, MetadataModel):
    """
        Modelo que representa a un Evento especial
    """
    
    titulo = models.CharField(
        max_length=255,
        help_text="Títol de l'esdeveniment especial",
        verbose_name="Títol"
    )
    
    slug = models.SlugField(
        unique=True,
        editable=False,
        help_text="Slug automàtic generat a partir del títol",

    )

    color = ColorField(
        default='#FFFFFF',
        verbose_name="Color"
    )

    fecha_evento = models.DateField(
        default=timezone.now,
        help_text="Data de l'esdeveniment",
        verbose_name="Data de l'esdeveniment"
    )

    fecha_fin = models.DateField(
        default=timezone.now,
        help_text="Data de finalització de l'esdeveniment",
        verbose_name="Data de finalització"
    )

    publicado = models.BooleanField(
        default=False,
        help_text="Indica si l'esdeveniment especial està publicat",
        verbose_name="Publicat"
    )

    descripcion_larga = RichTextField(
        help_text="Descripció llarga de l'esdeveniment especial",
        null=True,
        blank=True,
        verbose_name="Descripció llarga"
    )

    descripcion_corta = RichTextField(
        help_text="Descripció curta de l'esdeveniment especial",
        null=True,
        blank=True,
        verbose_name="Descripció curta"
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="categoria",
        help_text="Selecciona la categoria vinculada",
        verbose_name="Categoria"
    )

    logo_especial = models.ImageField(
        upload_to='eventos_especiales/',
        help_text="Logotip especial per a l'esdeveniment",
        null=True,
        blank=True,
        verbose_name="Logotip especial"
    )

    imagen_especial = models.ImageField(
        upload_to='eventos_especiales/',
        help_text="miniatura que serveix per les seleccions i per les metadades",
        null=True,
        blank=True,
        verbose_name="Miniatura d'esdeveniment especial"
    )


    mostrar_ahorro = models.BooleanField(
    default=False,
    help_text="Marca si vols que es mostri els preus",
    verbose_name="Mostrar l'estalvi"
    )
    
    agendas = models.ManyToManyField(
        Post,
        blank=True,
        related_name="esdeveniment",
        help_text="Selecciona tots els esdeveniments vinculats amb l'event",
        verbose_name="esdeveniment"
    )

    medida_economica = models.ForeignKey(
        MedidaEconomica,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Mesura o pla econòmic per l'esdeveniment especial (opcional)",
        verbose_name="Mesura econòmica"
    )

    parallax = models.ForeignKey(
        Parallax,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Parallax relacionat amb l'esdeveniment especial (opcional)",
        verbose_name="Parallax"
    )

    videos = models.ManyToManyField(
        Video,
        blank=True,
        help_text="Videos relacionats amb l'esdeveniment especial (opcional)",
        verbose_name="Vídeos"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="Tags"
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
            if EventoEspecial.objects.filter(slug=self.slug).exclude(id=self.id).exists():
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
        return self.fecha_evento > timezone.now().date()
    
    def has_ended(self):
        """
        Retorna True si el evento ha terminado (ha pasado la fecha de finalización).
        """
        return self.fecha_fin < timezone.now().date()
    
    def get_absolute_url(self):
        return reverse('eventos_especiales:evento_especial', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.titulo
    
    def get_logo_absolute_url(self):
        if self.logo_especial.url:
            return settings.DOMAIN_URL + self.logo_especial.url
        else:
            return None
    
    class Meta:
        verbose_name_plural = "Esdeveniments Especials"


class EventoEspecialGaleriaImagen(models.Model):
    evento_especial = models.ForeignKey(
        EventoEspecial, on_delete=models.CASCADE, default=None)
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post: {self.evento_especial.titulo} - Imagen: {self.imagen}"
    
    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = EventoEspecial.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)



class EventoFichero(models.Model):
    evento = models.OneToOneField(
        EventoEspecial,
        on_delete=models.CASCADE,
        null=True
    )

    fichero = models.OneToOneField(
        Fichero,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Evento: {self.evento} - Fichero: {self.fichero}"

    def delete(self, *args, **kwargs):
        # Eliminar la imagen asociada antes de eliminar el objeto SubBlogImagen
        # self.evento.delete() .-.
        self.fichero.delete()
        super().delete(*args, **kwargs)





class EventoMensaje(models.Model):
    """
        Modelo que vincula el mensaje autor y el evento especial
    """
    evento_especial = models.ForeignKey(
        EventoEspecial,
        on_delete=models.CASCADE,
        verbose_name="esdeveniment especial"
    )
    mensaje = models.ForeignKey(
        Mensaje,
        on_delete=models.CASCADE,
        verbose_name="missatge"
    )
    def __str__(self):
        return f"Esdeveniment: {self.evento_especial.titulo} - Autor: {self.mensaje.autor.nombre}"
    class Meta:
        unique_together = ('evento_especial', 'mensaje')  # Asegura que la combinación de evento y mensaje sea única
        
    def __str__(self):
        return f"{self.evento_especial.titulo} - {self.mensaje.titulo}"
