from django.db import models

from django.contrib.auth import get_user_model
from blog.models import Post
from multimedia_manager.models import Imagen

User = get_user_model()

# Create your models here.


class Agenda(Post):
    ubicacion = models.CharField(max_length=255)
    descripcion_corta = models.CharField(max_length=255)
    TIPO_EVENTO_CHOICES = (
        ('musica', 'Música'),
        ('teatre', 'Teatre'),
        ('exposicio', 'Exposició'),
        ('festes','festes'),
        ('cinema', 'Cinema'),
        ('dansa', 'Dansa'),
        ('visites_guiades','Visites guiades'),
        ('activitats_turistiques','Activitats turístiques'),
        ('altres', 'Altres (Otros)'),
    )

    # Resto de campos de Agenda

    tipo_evento = models.CharField(
        max_length=30,
        choices=TIPO_EVENTO_CHOICES,
        help_text="Selecciona el tipo de evento",
        default='altres',
    )   

    class Meta:
        verbose_name = "Agenda"
        verbose_name_plural = "Agendas"


class AgendaGaleriaImagen(models.Model):
    agenda = models.ForeignKey(
        Agenda, on_delete=models.CASCADE, default=None)
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"Agenda: {self.agenda.titulo} - Imagen: {self.imagen}"
    
    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = Agenda.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)