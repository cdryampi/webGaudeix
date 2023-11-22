from django.db import models

from django.contrib.auth import get_user_model
from blog.models import Post
from multimedia_manager.models import Imagen
from map.models import MapPoint
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import timedelta, datetime, time
from django.utils import timezone



User = get_user_model()

# Create your models here.



class Agenda(Post):

    entradas = models.BooleanField(
        default=False,
        help_text="Hi ha entrades?",
        verbose_name="Entrades"
    )

    ubicacion = models.ForeignKey(
        MapPoint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ubicació',
        help_text="ubicació",
        verbose_name="ubicació"
    )

    descripcion_corta = models.CharField(
        max_length=255,
        verbose_name="Descripció curta"
    )

    TIPO_EVENTO_CHOICES = (
        ('musica', 'Música'),
        ('teatre', 'Teatre'),
        ('exposicio', 'Exposició'),
        ('festes','festes'),
        ('cinema', 'Cinema'),
        ('dansa', 'Dansa'),
        ('visites_guiades','Visites guiades'),
        ('activitats_turistiques','Activitats turístiques'),
        ('xerrades','xerrades'),
        ('joves','joves'),
        ('altres', 'Altres (Otros)'),
    )

    # Resto de campos de Agenda

    tipo_evento = models.CharField(
        max_length=30,
        choices=TIPO_EVENTO_CHOICES,
        help_text="Selecciona el tipus d'esdeveniment",
        default='altres',
        verbose_name=_("Tipus d'esdeveniment")
    )   

    class Meta:
        verbose_name = "Agenda"
        verbose_name_plural = "Agendas"

    def get_absolute_url(self):
            return reverse('agenda:detalle_agenda', kwargs={'slug': self.slug})


class VariationAgenda(models.Model):

    agenda = models.ForeignKey(
        Agenda, 
        on_delete=models.CASCADE,
        verbose_name="Agenda"
    )

    fecha = models.DateField(
        default=timezone.now,
        verbose_name="Data"
    )

    hora = models.TimeField(
        default=timezone.now,
        verbose_name="Hora"
    )


    def generate_google_calendar_link(self):
        # Obtener la fecha y hora de inicio
        from personalizacion.models import Personalizacion

        personalizacion = Personalizacion.objects.first()
        horario = personalizacion.horario
        data_fin = personalizacion.hora_agenda_fin
        fecha_inicio = self.fecha  # Fecha en tu modelo
        hora_inicio = self.hora  # Hora en tu modelo

        # Combinar la fecha y hora para obtener la fecha y hora de inicio completa
        fecha_hora_inicio = datetime.combine(fecha_inicio, hora_inicio)

        if horario == 'hivern':
            # Convertir data_fin (TimeField) a timedelta
            
            fecha_hora_inicio = fecha_hora_inicio + timedelta(hours=-1)

        # Calcular la fecha y hora de fin sumando 2 horas
        data_fin_timedelta = timedelta(hours=data_fin.hour, minutes=data_fin.minute)
        fecha_hora_fin = fecha_hora_inicio + data_fin_timedelta

        if fecha_hora_fin.time() >= time(23,59):
            fecha_hora_fin = fecha_hora_inicio
        # Formatear las fechas y horas en el formato adecuado
        fecha_hora_inicio_str = fecha_hora_inicio.strftime("%Y%m%dT%H%M%SZ")
        fecha_hora_fin_str = fecha_hora_fin.strftime("%Y%m%dT%H%M%SZ")

        # Crear el enlace de Google Calendar
        return f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={self.agenda.titulo}&dates={fecha_hora_inicio_str}/{fecha_hora_fin_str}&details={self.agenda.descripcion_corta}&location={self.agenda.ubicacion}"


    def __str__(self):
            return f"Agenda: {self.agenda.titulo}"
    
    class Meta:
        verbose_name = "Variació d'agenda"
        verbose_name_plural = "Variacions"


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
        blank=True,
        verbose_name="Durada"
    )
    pendiente = models.FloatField(
        help_text="Pendent de la ruta (en metres)",
        null=True,
        blank=True,
        verbose_name="Pendent"
    )
    distancia = models.FloatField(
        help_text="Distància de la ruta (en quilòmetres)",
        null=True,
        blank=True,
        verbose_name="Distància"
    )
    tema = models.CharField(
        max_length=255,
        help_text="Tema de la ruta",
        null=True,
        blank=True,
        verbose_name="Tema"
    )
    actividad = models.CharField(
        max_length=255,
        help_text="Activitat de la ruta",
        null=True,
        blank=True,
        verbose_name="Activitat"
    )
    valoracion = models.FloatField(
        help_text="Valoració de la ruta",
        null=True,
        blank=True,
        verbose_name="Valoració"
    )

    tipologia = models.CharField(
        max_length=20,
        choices=TIPOLOGIA_CHOICES,
        default='circular',
        help_text="Tipologia de la ruta",
        verbose_name="Tipologia",
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
        help_text="Mapes que formen part de l'itinerari",
        verbose_name="Mapes d'itinerari"
    )

    enlace_natura_local = models.URLField(
        default= "https://naturalocal.net/ca/destins/barcelona/cabrera-de-mar#rutes",
        help_text= "Afegeix l'enllaç exacte cap a Natura Local.",
        verbose_name="Enllaç a Natura Local"
    )

    def __str__(self):
        return f"Ruta: {self.titulo}"


class CertificadoTurismoSostenible(models.Model):
    ODS_CHOICES = (
        ('ods_1', "Fi de la pobresa"),
        ('ods_2', "Fam zero"),
        ('ods_3', "Salut i benestar"),
        ('ods_4', "Educació de qualitat"),
        ('ods_5', "Igualtat de gènere"),
        ('ods_6', "Aigua neta i sanejament"),
        ('ods_7', "Energia assequible i no contaminant"),
        ('ods_8', "Treball decent i creixement econòmic"),
        ('ods_9', "Indústria, innovació i infraestructura"),
        ('ods_10', "Reducció de les desigualtats"),
        ('ods_11', "Ciutats i comunitats sostenibles"),
        ('ods_12', "Consum i produccions responsables"),
        ('ods_13', "Acció pel clima"),
        ('ods_14', "Vida submarina"),
        ('ods_15', "Vida d'ecosistemes terrestres"),
        ('ods_16', "Pau, justícia i institucions sòlides"),
        ('ods_17', "Aliances per assolir els objectius"),
        ('altres', "Altres")
    )

    nombre = models.CharField(
         max_length=100,
         verbose_name='títol',
         help_text='Nom del certificat del certificat.'
    )
    descripcion = models.TextField(
        verbose_name="Descripció",
        help_text="Afegeix una descripció pel certificat.",
        null=True,
        blank=True
    )
    logo = models.ImageField(
        upload_to='logos_certificados/',
        verbose_name="Logo",
        help_text="Afegeix un Logo pel certificat.",
    )
    ods_relacionados = models.CharField(
        choices= ODS_CHOICES,
        null=True,
        blank=True,
        verbose_name="ODS relacionat",
        help_text="Vincula amb el ODS que té relació el certificat"
    )
    enlace_externo = models.URLField(
        null=True,
        blank=True,
        help_text="Enllaç extern",
        verbose_name="Enllaç extern"
    )  # Enllaç extern (opcional)

    class Meta:
        verbose_name = "Certificat"
        verbose_name_plural = "Certificats"

    def __str__(self):
        return self.nombre


class VisitaGuiada(Post):

    PUBLICO_RECOMENDADO_CHOICES = (
        ('nens', _('Nens')),
        ('joves', _('Joves')),
        ('adults', _('Adults')),
        ('todos', _('Totes les edats')),
    )

    MOSTRAR_CALENDARIO_CHOICES = (
        ('si', _('Sí')),
        ('no', _('No')),
    )

    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Preu de la visita (en euros)",
        verbose_name="Preu"
    )

    duracion = models.DurationField(
        default=timedelta(days=2), 
        help_text="Duració de la visita (en format DD HH:MM:SS)",
        verbose_name="Duració"
    )

    fecha_inicio = models.DateField(
        default=timezone.now, 
        help_text="Data d'inici del rang",
        verbose_name="Data d'inici"
    )

    fecha_fin = models.DateField(
        default=timezone.now() + timezone.timedelta(days=7),
        help_text="Data de finalització del rang",
        verbose_name="Data de finalització"
    )

    mostrar_calendario = models.CharField(
        max_length=2,
        choices=MOSTRAR_CALENDARIO_CHOICES,
        default='no',
        help_text="Indica si es mostrarà el calendari en la plantilla",
        verbose_name="Mostrar calendari"
    )

    publico_recomendado = models.CharField(
        max_length=20,
        choices=PUBLICO_RECOMENDADO_CHOICES,
        default='todos',
        help_text="Públic recomanat per a la visita",
        verbose_name="Públic recomanat"
    )

    mapa = models.ForeignKey(
        MapPoint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='visitas_mapa',
        help_text="Mapa relacionat amb la visita",
        verbose_name="Mapa"
    )
    
    agendas = models.ManyToManyField(
        Agenda,
        related_name='visitas_guiadas',
        blank=True,
        help_text="Agendes relacionades amb la visita",
        verbose_name="Agendes"
    )

    certificados = models.ManyToManyField(
        CertificadoTurismoSostenible,
        blank=True,
        help_text="Afegeix els certificats de turisme sostenible que fas servir per la visita guiada.",
        verbose_name="Certificat"
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
