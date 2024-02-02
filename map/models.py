from django.db import models
from blog.models import Post
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _


#from django.contrib.gis.db import models as gis_models

ICON_CHOICES = (
    
    ('station', 'Estació'),
    ('restaurant', 'Restaurant'),
    ('library', 'Biblioteca'),
    ('hotel', 'Hotel'),
    ('town-hall', 'Ajuntament'),
    ('theater', 'Centre Cultural'),
    ('sport', 'Esports'),
    ('serveis','Serveis'),
    ('transports','Transports'),
    ('aparcaments','Aparcaments'),
    ('platges','Platges'),
    ('informació',"Punt d'informació"),
    ('jaciments', 'Jaciments arqueològics'),
    ('patrimoni', 'Patrimoni cultural'),
    ('flora-i-fauna','flora i fauna')
    # Agrega más opciones según tus necesidades
)


class MapPointManager(models.Manager):

    def punto_referencia_principal(self):
        return self.get(titulo='Punto de Referencia')


class MapPoint(Post):
    """
    Clase que representa a un lugar de Cabrera de Mar
    """
    latitud = models.FloatField(
        help_text='Introduïu la latitud (copiada de Google Maps)',
        verbose_name='Latitud'
    )
    longitud = models.FloatField(
        help_text='Introduïu la longitud (copiada de Google Maps)',
        verbose_name='Longitud'
    )
    icono = models.CharField(
        max_length=100,
        choices=ICON_CHOICES
    )
    municipio = models.CharField(
        max_length=100,
        default='Cabrera de Mar',
        editable=False,
        help_text=_('Municipi'),
        verbose_name='Municipi'
    )
    comarca = models.CharField(
        max_length=100,
        default='Maresme',
        editable=False,
        help_text=_('Comarca'),
        verbose_name='Comarca'
    )
    comunidad_autonoma = models.CharField(
        max_length=100,
        default='Catalunya',
        editable=False,
        help_text=_('Comunitat Autònoma'),
        verbose_name='Comunitat Autònoma'
    )
    pais = models.CharField(
        max_length=100,
        default='Espanya',
        editable=False,
        help_text=_('País'),
        verbose_name='País'
    )
    codigo_postal = models.CharField(
        max_length=10,
        default='08349',
        editable=False,
        help_text=_('Codi postal'),
        verbose_name='Codi postal'
    )
    calle = models.CharField(
        max_length=255,
        editable=True,
        help_text=_('Carrer'),
        null=True,
        blank=True,
        verbose_name='Carrer'
    )
    contenido_adicional = RichTextField(
        blank=True,
        null=True,
        help_text='Texto adicional',
        verbose_name='Contingut addicional'
    )
    enlace_google_maps = models.URLField(
        blank=True,
        null=True,
        help_text='Enllaç a Google Maps',
        verbose_name='Enllaç a Google Maps'
    )
    objects = MapPointManager()

    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = 'Punt de mapa'
        verbose_name_plural = 'Punts de mapa'