from django.db import models

from django.utils.text import slugify
from colorfield.fields import ColorField
from core.models import BaseModel, MetadataModel
from multimedia_manager.models import Fichero, Imagen
from personalizacion.models import Parallax, Video, Carrusel
from agenda.models import Agenda
from ckeditor.fields import RichTextField
from django.utils import timezone
# Create your models here.








class EventoEspecial(BaseModel, MetadataModel):
    
    
    titulo = models.CharField(max_length=255, help_text="Títol de l'esdeveniment especial")
    slug = models.SlugField(unique=True, editable=False, help_text="Slug automàtic generat a partir del títol")
    color = ColorField(default='#FFFFFF')
    
    fecha_evento = models.DateField(
        default=timezone.now,
        help_text="Data de l'esdeveniment"
    )

    publicado = models.BooleanField(
        default=False,
        help_text="Indica si l'esdeveniment especial està publicat"
    )

    descripcion_larga = RichTextField(
        help_text="Descripció llarga de l'esdeveniment especial",
        null=True,
        blank=True
    )
    descripcion_corta = RichTextField(
        help_text="Descripció curta de l'esdeveniment especial",
        null=True,
        blank=True
    )

    logo_especial = models.ImageField(
        upload_to='eventos_especiales/',
        help_text="Logotip especial per a l'esdeveniment"
    )
    
    imagenes = models.ManyToManyField(
        Imagen,
        blank=True,
        related_name="eventos_especiales",
        help_text="Imatges de l'esdeveniment especial (mínim 4)"
    )

    agendas = models.ManyToManyField(
        Agenda,
        blank=True,
        related_name="agenda",
        help_text="Selecciona tots els esdeveniments vinculats amb l'event"
    )

    parallax = models.ForeignKey(
        Parallax,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Parallax relacionat amb l'esdeveniment especial (opcional)"
    )
    videos = models.ManyToManyField(
        Video,
        blank=True,
        help_text="Videos relacionats amb l'esdeveniment especial (opcional)"
    )
    carruseles = models.ManyToManyField(
        Carrusel,
        blank=True,
        help_text="Carrussells relacionats amb l'esdeveniment especial (opcional)"
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
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name_plural = "Esdeveniments Especials"





class EventoFichero(models.Model):
    evento = models.OneToOneField(
        EventoEspecial, on_delete=models.CASCADE, null=True)
    fichero = models.OneToOneField(Fichero, on_delete=models.CASCADE)

    def __str__(self):
        return f"Evento: {self.evento} - Fichero: {self.fichero}"

    def delete(self, *args, **kwargs):
        # Eliminar la imagen asociada antes de eliminar el objeto SubBlogImagen
        self.evento.delete()
        super().delete(*args, **kwargs)
