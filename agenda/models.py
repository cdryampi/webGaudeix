from django.db import models

from django.contrib.auth import get_user_model
from blog.models import Post
from multimedia_manager.models import Imagen
from map.models import MapPoint
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

# Create your models here.



class Agenda(Post):
    entradas = models.BooleanField(default=False, help_text="Hi ha entrades?")
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)
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
        ('xarrades','xarrades'),
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



class Ruta(Post):
    
    TIPOLOGIA_CHOICES = (
        ('circular', 'Circular'),
        ('antihorario', 'Antihorari'),
        # Agrega más opciones según tus necesidades
    )

    DIFICULTAD_CHOICES = (
        ('facil', 'Fàcil'),
        ('media', 'Mitjana'),
        ('dificil', 'Difícil'),
        # Agrega más opciones según tus necesidades
    )

    duracion = models.DurationField(
        help_text="Durada de la ruta",
        null=True,
        blank=True
    )
    pendiente = models.FloatField(
        help_text="Pendent de la ruta (en metres)",
        null=True,
        blank=True
    )
    distancia = models.FloatField(
        help_text="Distància de la ruta (en quilòmetres)",
        null=True,
        blank=True
    )
    tema = models.CharField(
        max_length=255,
        help_text="Tema de la ruta",
        null=True,
        blank=True
    )
    actividad = models.CharField(
        max_length=255,
        help_text="Activitat de la ruta",
        null=True,
        blank=True
    )
    valoracion = models.FloatField(
        help_text="Valoració de la ruta",
        null=True,
        blank=True
    )

    tipologia = models.CharField(
        max_length=20,
        choices=TIPOLOGIA_CHOICES,
        default='circular',
        help_text="Tipologia de la ruta",
        verbose_name="Tipologia"
    )

    dificultad = models.CharField(
        max_length=20,
        choices=DIFICULTAD_CHOICES,
        default='facil',
        help_text="Dificultat de la ruta",
        verbose_name="Dificultat"
    )

    punto_inicio = models.ForeignKey(
        MapPoint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rutas_punto_inicio',
        help_text="Punt d'inici de la ruta",
        verbose_name="Punt d'inici"
    )

    mapas_itinerario = models.ManyToManyField(
        MapPoint,
        related_name='rutas_itinerario',
        blank=True,
        help_text="Mapes que formen part de l'itinerari"
    )

    enlace_natura_local = models.URLField(
        default= "https://naturalocal.net/ca/destins/barcelona/cabrera-de-mar#rutes",
        help_text= "Afegeix l'enllaç exacte cap a Natura Local."
    )

    def __str__(self):
        return f"Ruta: {self.titulo}"

class VisitaGuiada(Post):
    precio = models.DecimalField(max_digits=8, decimal_places=2, help_text="Preu de la visita (en euros)")
    duracion = models.DurationField(default=timedelta(days=2), help_text="Duració de la visita (en format DD HH:MM:SS)")

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



    def get_absolute_url(self):
        return reverse('agenda:visites-guiades', kwargs={'slug': self.slug})


    def __str__(self):
        duracion_dias = self.duracion.days
        duracion_horas = self.duracion.seconds // 3600
        return f"Visita Guiada : {self.titulo}"
