from django.db import models
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
    ('patrimoni', 'Patrimoni cultural')
    # Agrega más opciones según tus necesidades
)


class MapPointManager(models.Manager):

    def punto_referencia_principal(self):
        return self.get(titulo='Punto de Referencia')


class MapPoint(models.Model):

    titulo = models.CharField(max_length=100)
    latitud = models.FloatField(help_text='Introduïu la latitud (copiada de Google Maps)')
    longitud = models.FloatField(help_text='Introduïu la longitud (copiada de Google Maps)')
    publicado = models.BooleanField(default=False, help_text="publicat?")
    icono = models.CharField(max_length=100, choices=ICON_CHOICES)
    objects = MapPointManager()

    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = 'Punt de mapa'
        verbose_name_plural = 'Punts de mapa'