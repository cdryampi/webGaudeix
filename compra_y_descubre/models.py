from django.db import models
from personalizacion.models import Parallax, Video, Carrusel
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

# Create your models here.

class CompraDescubre(BaseModel, MetadataModel):
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
    negocis = models.ManyToManyField(
        MapPoint,
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

    def save(self, *args, **kwargs):
        if not self.slug or not self.id:
            self.slug = slugify(self.titulo)
        else:
            # Verificar si el slug ya existe y el objeto ya existe
            if CompraDescubre.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                # Generar un slug único basado en la fecha y hora actual
                timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
                self.slug = f"{self.slug}-{timestamp}"
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
        verbose_name_plural = "Esdeveniments Especials Compra i descubre"





class CompaDescubrePasosImagen(models.Model):
    compadescubre = models.ForeignKey(
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
        return f"Post: {self.compadescubre.titulo} - Imagen: {self.imagen}"
    
    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = CompaDescubrePasosImagen.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)




class CompraDescubreImagen(models.Model):
    """
    Modelo para asociar una imagen a un CompraDescubre.
    """
    compadescubre = models.OneToOneField(
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
        return f"CompraDescubre: {self.compadescubre} - Imagen: {self.imagen}"

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



class CompaDescubreFichero(models.Model):
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
