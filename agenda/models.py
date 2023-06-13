from django.db import models

from django.contrib.auth import get_user_model
from blog.models import Post
from multimedia_manager.models import Imagen
from map.models import MapPoint
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


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

    def get_absolute_url(self):
            return reverse('agenda:detalle_agenda', kwargs={'slug': self.slug})


class VisitaGuidada(Post):
    precio = models.DecimalField(max_digits=8, decimal_places=2, help_text="Preu de la visita (en euros)")
    duracion = models.DurationField(default='2 days', help_text="Duració de la visita (en format DD HH:MM:SS)")
    punto_inicio = models.ForeignKey(
        MapPoint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='visitas_punto_inicio',
        help_text="Mapa relacionat amb la visita"
    )

    PUBLICO_RECOMENDADO_CHOICES = (
        ('nens', _('Nens')),
        ('joves', _('Joves')),
        ('adults', _('Adults')),
        ('todos', _('Totes les edats')),
    )
    publico_recomendado = models.CharField(
        max_length=20,
        choices=PUBLICO_RECOMENDADO_CHOICES,
        default='todos',
        help_text="Públic recomanat per a la visita"
    )

    mapa = models.ForeignKey(
        MapPoint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='visitas_mapa',
        help_text="Mapa relacionat amb la visita"
    )
    
    agendas = models.ManyToManyField(
        Agenda,
        related_name='visitas_guiadas',
        blank=True,
        help_text="Agendes relacionades amb la visita"
    )

    # Resto de campos adicionales de VisitaGuidada
    
    class Meta:
        verbose_name = "Visita Guiada"
        verbose_name_plural = "Visitas Guiadas"
    
    def __str__(self):
        return f"Visita Guiada : {self.titulo}"



class VisitaGuidadaGaleriaImagen(models.Model):
    visita_guidada = models.ForeignKey(
        VisitaGuidada, on_delete=models.CASCADE, default=None)
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"Visita Guiada: {self.visita_guidada} - Imagen: {self.imagen}"
    
    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = VisitaGuidadaGaleriaImagen.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)


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