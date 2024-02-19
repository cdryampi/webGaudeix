from django.db import models
from django.core.validators import MaxLengthValidator
from colorfield.fields import ColorField


# Create your models here.
class Topbar(models.Model):
    # modelo que representa un TopBar
    titulo = models.CharField(
        max_length=100,
        help_text="Títol del TopBar",
        verbose_name="Títol del TopBar"
    )  # Títol del TopBar
    descripcion = models.TextField(
        validators=[MaxLengthValidator(200)],
        help_text="Descripció del TopBar",
        verbose_name="Descripció del TopBar"
    )  # Descripció del TopBar (màxim 200 caràcters)
    descripcion_corta_movil = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Descripció curta per a mòbils (màxim 50 paraules)",
        verbose_name="Descripció curta per a mòbils"
    )  # Descripció curta per a mòbils (opcional)

    enlace_externo = models.URLField(
        null=True,
        blank=True,
        help_text="Enllaç extern",
        verbose_name="Enllaç extern"
    )  # Enllaç extern (opcional)

    titulo_externo = models.CharField(
        max_length=25,
        help_text="nom enllaç màxim 20 paraules",
        null=True,
        blank=True,
        verbose_name="Nom enllaç"
    )

    fondo = ColorField(
        default='#FFFFFF',
        help_text="Color de fons del TopBar",
        verbose_name="Color de fons del TopBar"
    )  # Color de fons del TopBar

    texto_color = ColorField(
        default='#000000',
        help_text="Color del text del TopBar",
        verbose_name="Color del text del TopBar"
    )  # Color del text del TopBar

    publicado = models.BooleanField(
        default=False,
        help_text="Indica si el TopBar està publicat",
        verbose_name="TopBar publicat"
    )  # Indica si el TopBar està publicat
    
    def __str__(self):
        return self.titulo