from django.db import models

# Create your models here.
class RedSocial(models.Model):
    # modelo que representa una red social. Ejemplo Tiktok, Instagram, Facebook y Twitter.
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='redes_sociales',help_text='Imagen del icono de la red social (dimensiones recomendadas: 32x32 pixels)')
    link = models.URLField()

    def __str__(self):
        return self.titulo