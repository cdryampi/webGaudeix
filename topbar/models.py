from django.db import models
from django.core.validators import MaxLengthValidator

# Create your models here.
class Topbar(models.Model):
    # modelo que representa un TopBar
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(validators=[MaxLengthValidator(100)])  # Límite de 100 caracteres
    descripcion_corta_movil = models.CharField(max_length=50)
    enlace_externo = models.URLField()

    def __str__(self):
        return self.titulo