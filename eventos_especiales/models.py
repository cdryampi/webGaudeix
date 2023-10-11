from django.db import models

from django.utils.text import slugify
from colorfield.fields import ColorField
from core.models import BaseModel, MetadataModel
from multimedia_manager.models import Fichero, Imagen
from personalizacion.models import Parallax, Video, Carrusel
from agenda.models import Agenda
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.urls import reverse
from blog.models import Tag, Categoria, Post
from django.conf import settings

# Create your models here.

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
    
    agendas = models.ManyToManyField(
        Post,
        blank=True,
        related_name="esdeveniment",
        help_text="Selecciona tots els esdeveniments vinculats amb l'event",
        verbose_name="esdeveniment"
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

    carruseles = models.ManyToManyField(
        Carrusel,
        blank=True,
        help_text="Carrussells relacionats amb l'esdeveniment especial (opcional)",
        verbose_name="Carrussells"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="Tags"
    )
    
    def save(self, *args, **kwargs):
        if not self.slug or not self.id:
            self.slug = slugify(self.titulo)
        else:
            # Verificar si el slug ya existe y el objeto ya existe
            if EventoEspecial.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                # Generar un slug único basado en la fecha y hora actual
                timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
                self.slug = f"{self.slug}-{timestamp}"
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
        return settings.DOMAIN_URL + self.logo_especial.url
    
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
