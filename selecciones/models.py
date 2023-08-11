from django.db import models
from blog.models import Post
from eventos_especiales.models import EventoEspecial
# Create your models here.

class SeleccionDestacados(models.Model):
    
    titulo = models.CharField(max_length=100, help_text="Escriu un nom únic")
    publicado = models.BooleanField(default=False, help_text="Marca si vols que estigui despublicat.")
    coleccion = models.ManyToManyField(Post, related_name='seleccions', blank=True)
    eventos_especiales = models.ManyToManyField(EventoEspecial, related_name="seleccio_especial", blank=True, help_text="Selecciona els esdeveniments que vols que apareguin a la portada.")

    def __str__(self):
        return self.titulo