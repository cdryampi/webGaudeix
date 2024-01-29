from django.db import models
from colorfield.fields import ColorField

# Create your models here.
class RedSocial(models.Model):
    """ 
        modelo que representa una red social. Ejemplo Tiktok, Instagram, Facebook y Twitter.
    """
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='redes_sociales',help_text='Imagen del icono de la red social (dimensiones recomendadas: 32x32 pixels)')
    link = models.URLField()
    fondo = ColorField(default='#FFFFFF', help_text="Color de fons que vols")  # Color de fons del TopBar

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "xarxa social"
        verbose_name_plural = "xarxes socials"
