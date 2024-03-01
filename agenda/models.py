import re
from django.db import models
from django.contrib.auth import get_user_model
from blog.models import Post
from multimedia_manager.models import Imagen
from map.models import MapPoint
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import timedelta, datetime, time
from django.utils import timezone
from ckeditor.fields import RichTextField
from multimedia_manager.models import Audio
from django.core.exceptions import ValidationError
from gaudeix.settings import DOMAIN_URL 
from urllib.parse import urlparse, quote

User = get_user_model()

# Create your models here.

class Restaurante(Post):
    """
    Modelo que representa a un Restaurante.
    """
    TIPO_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('bar', 'Bar'),
        ('masia', 'Masia'),  # Longitud más larga que 10 caracteres
        ('guingueta', 'guingueta'),
    ]

    descripcion_corta = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Descripció curta"
    )
    tipo = models.CharField(
        max_length=20,  # Aumentado para ajustarse a la opción más larga
        choices=TIPO_CHOICES,
        verbose_name="Tipus de restaurant"
    )
    direccion = models.CharField(
        max_length=255,
        verbose_name="Direcció",
        help_text="Afegeix la dirrecció del allotjament"
    )
    telefono = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Telefon",
        help_text="Afegeix el telefón principal"
    )
    sitio_web = models.URLField(
        blank=True,
        null=True,
        verbose_name="Lloc web",
        help_text="Afegix el lloc web de l'empresa"
    )
    capacidad = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Capacitat",
        help_text="Máxim de persones."
    )
    horarios = models.TextField(
        blank=True,
        null=True,
        verbose_name="Horaris",
        help_text="Horaris de obertura i tancament"
    )
    google_maps_link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Enllaç del Google Maps",
        help_text="Afegeix l'enllaç cap a Google Maps."
    )
    latitud = models.FloatField(
        verbose_name="Latitud",
        help_text="Aquest Camp es opcional, si no l'afegeixes no es generarà el map.",
        blank=True,
        null=True,
    )
    longitud = models.FloatField(
        verbose_name="Longitud",
        help_text="Aquest Camp es opcional, si no l'afegeixes no es generarà el map.",
        blank=True,
        null=True,
    )
    pet_friendly = models.BooleanField(
        default=False,
        verbose_name="Admet mascotes",
        help_text="Indica si el restaurant admet mascotes."
    )
    opciones_vegetarianas = models.BooleanField(
        default=False,
        verbose_name="Opcions vegetarianes",
        help_text="Indica si el restaurant ofereix opcions vegetarianes."
    )
    wifi = models.BooleanField(
        default=False,
        verbose_name="WiFi disponible",
        help_text="Indica si el restaurant ofereix WiFi als clients."
    )
    apto_para_celiacos = models.BooleanField(
        default=False,
        verbose_name="Apte per a celíacs",
        help_text="Indica si el restaurant ofereix opcions per a celíacs."
    )
    terraza = models.BooleanField(
        default=False,
        verbose_name="Terrassa disponible",
        help_text="Indica si el restaurant disposa de terrassa."
    )
    menu_infantil = models.BooleanField(
        default=False,
        verbose_name="Menú infantil",
        help_text="Indica si el restaurant ofereix menú infantil."
    )
    
    accessibilitat = models.BooleanField(
        default=False,
        verbose_name="Accessibilitat per a persones amb discapacitat",
        help_text="Indica si el restaurant compta amb accessibilitat per a persones amb discapacitat."
    )

    parking = models.BooleanField(
        default=False,
        verbose_name="Aparcament",
        help_text="Indica si el restaurant compta amb estacionament o aparcament."
    )


    class Meta:
        verbose_name = "restaurant"
        verbose_name_plural = "restaurants"

    def __str__(self):
        # Asegúrate de que 'tipo' se traduce correctamente desde TIPO_CHOICES
        tipo_display = dict(Restaurante.TIPO_CHOICES).get(self.tipo, "Tipo no especificado")
        return f"{tipo_display}: {self.titulo}"



class Alojamiento(Post):
    """
    Modelo que representa a un Alojamiento.
    """
    TIPO_CHOICES = [
        ('hotel', 'Hotel'),
        ('alberg', 'Alberg'),
        ('turístic', 'Allotjament turístic'),  # Longitud más larga que 10 caracteres
        ('autocaravanes', 'Autocaravanes'),
    ]

    tipo = models.CharField(
        max_length=20,  # Aumentado para ajustarse a la opción más larga
        choices=TIPO_CHOICES,
        verbose_name="Tipus d'Allotjament"
    )
    direccion = models.CharField(
        max_length=255,
        verbose_name="Direcció",
        help_text="Afegeix la dirrecció del allotjament"
    )
    telefono = models.CharField(
        max_length=20, null=True,
        blank=True,
        verbose_name="Telefon",
        help_text="Afegeix el telefón principal"
    )
    sitio_web = models.URLField(
        blank=True,
        null=True,
        verbose_name="Lloc web",
        help_text="Afegix el lloc web de l'empresa"
    )
    capacidad = models.IntegerField(
        verbose_name="Capacitat",
        help_text="Máxim de persones."
    )
    horarios = models.TextField(
        blank=True,
        null=True,
        verbose_name="Horaris",
        help_text="Horaris de obertura i tancament"
    )
    google_maps_link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Enllaç del Google Maps",
        help_text="Afegeix l'enllaç cap a Google Maps."
    )
    latitud = models.FloatField(
        verbose_name="Latitud",
        help_text="Aquest Camp es opcional, si no l'afegeixes no es generarà el map.",
        blank=True,
        null=True,
    )
    longitud = models.FloatField(
        verbose_name="Longitud",
        help_text="Aquest Camp es opcional, si no l'afegeixes no es generarà el map.",
        blank=True,
        null=True,
    )
    pet_friendly = models.BooleanField(
        default=False,
        verbose_name="Pet Friendly",
    )
    wifi = models.BooleanField(
        default=False,
        verbose_name="WiFi"
    )
    adaptado_movilidad_reducida = models.BooleanField(
        default=False, 
        verbose_name="Adaptat per a persones amb mobilitat reduïda",
        help_text="Indica si l'allotjament està adaptat per a persones amb mobilitat reduïda."
    )
    parking_gratis = models.BooleanField(
        default=False, 
        verbose_name="Pàrquing gratuït",
        help_text="Indica si l'allotjament ofereix pàrquing gratuït."
    )
    habitaciones_sin_humo = models.BooleanField(
        default=False, 
        verbose_name="Habitacions sense fum",
        help_text="Indica si l'allotjament disposa d'habitacions lliures de fum."
    )
    servicio_habitaciones = models.BooleanField(
        default=False, 
        verbose_name="Servei d'habitacions",
        help_text="Indica si l'allotjament ofereix servei d'habitacions."
    )

    class Meta:
        verbose_name = "allotjament"
        verbose_name_plural = "allotjaments"

    def __str__(self):
        # Asegúrate de que 'tipo' se traduce correctamente desde TIPO_CHOICES
        tipo_display = dict(Alojamiento.TIPO_CHOICES).get(self.tipo, "Tipo no especificado")
        return f"{tipo_display}: {self.titulo}"



class Idioma(models.Model):
    """
        Modelo que representa un idioma o un lenguaje como el inclusivo.
    """
    IDIOMA_CHOICES = [
        ('cat', 'Català', 'fa-icon-for-catalan'),  # Reemplaza con el ícono correcto
        ('es', 'Espanyol', 'fa-flag-spain'),
        ('en', 'Anglès', 'fa-flag-usa'),
        ('fr', 'Francès', 'fa-flag-france'),
        ('it', 'Italià', 'fa-flag-italy'),  # Asume un ícono para Italia
        ('de', 'Alemany', 'fa-flag-germany'),  # Asume un ícono para Alemania
        ('pt', 'Portuguès', 'fa-flag-portugal'),  # Asume un ícono para Portugal
        ('ar', 'Àrab', 'fa-flag-saudi-arabia'),  # Asume un ícono para Arabia Saudita
        ('fem', 'Feminista', 'fa-icon-for-feminista'),
        ('au', 'autisme', 'fa-icon-for-autisme'),
        ('inc', 'inclusiu', 'fa-icon-for-inc')
        # ... más opciones según sea necesario
    ]
    nombre = models.CharField(
        max_length = 100,
        choices=[(code, f"{name} ({icon})") for code, name, icon in IDIOMA_CHOICES],
        verbose_name="Nom de l'idioma.",
        help_text="Nom de l'idioma PE: espanyol, català o altres com llenguatge inclusiu pels sords u/o altres llenguatges."
    )
    codigo = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Codi",
        help_text="Afegeix un codi únic per identificar l'idioma."
    )
    descripcion = RichTextField(
        help_text="Descripció pels usuaris a la plantilla de l'agenda.",
        null=True,
        blank=True,
        verbose_name="Descripció"
    )

    def __str__(self):
            return f"Idioma: {self.nombre}"

    def get_icon_class(self):
            for code, name, icon in self.IDIOMA_CHOICES:
                if self.codigo == code:
                    return icon
            return ""  # Devuelve una cadena vacía si no se encuentra ninguna coincidencia


    class Meta:
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomes"




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

    idiomas = models.ManyToManyField(
        Idioma,
        related_name='idiomes',
        blank=True,
        help_text="Idiomes que són disponibles per l'agenda.",
        verbose_name="idiomes"
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

    playlist = models.ManyToManyField(
        'PlaylistRuta',
        verbose_name="Playlist",
        blank=True,
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






class PlayListRuta(models.Model):
    """
        clase que reprsenta a una playlist
    """
    nom_intern = models.CharField(
        help_text="Afegiex un nom intern",
        verbose_name="nom intern",
        max_length=100,
    )

    idioma = models.ForeignKey(
        Idioma,
        on_delete=models.CASCADE,
        default = None,
        verbose_name="Idioma"
    )

    orden = models.PositiveIntegerField(default=0, verbose_name="Ordre")


    def __str__(self):
        return f"{self.nom_intern} - Idioma: {self.idioma}"
    
    class Meta:
        ordering = ['orden']
        verbose_name = "PlayList"
        verbose_name_plural = "PlayList"

class AudioRuta(models.Model):
    
    """
        Clase que representa el vinculo entre Ruta y el audio
    """

    playlist = models.ForeignKey(
         PlayListRuta,
         on_delete=models.CASCADE,
         verbose_name="playlist",
         default =None
    )

    audio = models.ForeignKey(
        Audio,
        on_delete=models.CASCADE,
        verbose_name="Àudio de la ruta"
    )

    link_unico = models.CharField(
        unique=True,  # Hace que el campo sea único
        blank=True,
        null=True,
        verbose_name="Afegeix un enllaç unic",
        help_text="Afegeix un enllaç 'https://gaudeixcabrera.cat/redirect/meu_fitxer.mp3'",
    )

    orden = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    def __str__(self):
        return f"Ruta: {self.playlist.nom_intern} - Àudio: {self.audio}"
    

    def delete(self, *args, **kwargs):
        self.audio.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar el audio anterior si se cambia el audio
        if self.pk:
            old_instance = AudioRuta.objects.get(pk=self.pk)
            if old_instance.audio != self.audio and old_instance.audio:
                old_instance.audio.delete()
        super().save(*args, **kwargs)

    def clean(self):
        # Verificar que la URL cumple con el formato deseado
        if self.link_unico:
            parsed_url = urlparse(self.link_unico)
            path_codificado = quote(parsed_url.path)  # Codifica la ruta para permitir caracteres especiales
            url_codificada = f'{parsed_url.scheme}://{parsed_url.netloc}{path_codificado}'
            
            # Actualiza el patrón para permitir caracteres codificados en la ruta
            url_pattern = rf'^{re.escape(DOMAIN_URL)}/redirect/[\w%.-]+(\.\w{{2,4}})?$'
            if not re.match(url_pattern, url_codificada):
                raise ValidationError("La URL no cumple con el formato requerido.")
        
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Àudio"
        verbose_name_plural = "Àudios"


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
