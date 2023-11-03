from ckeditor.fields import RichTextField
from core.models import BaseModel

from django.db import models

class RegistroError(BaseModel):
    """
        Modelo que representa a una indicencia en el proyecto
    """

    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name="data"
    )

    descripcion = models.TextField(
        blank=True,
        verbose_name="Traceback del problema"
    )
    
    titulo = models.TextField(
        editable=False, 
        null=True,
        verbose_name='Títol'
    )

    nota =RichTextField(
        help_text="Explicació de l'error i la seva solució",
        null=True,
        blank=True,
        verbose_name="Notes del problema"
    )

    resuelto = models.BooleanField(
        default=False,
        verbose_name="Resolt"
    )  # Campo para marcar como resuelto

    def __str__(self):
        return f"Error en {self.titulo}"
    
    class Meta:
        verbose_name = "Registre d'errors."
        verbose_name_plural = "Registre d'errors."