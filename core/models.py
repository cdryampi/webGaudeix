from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BaseModel(models.Model):
    """
    Modelo base que contiene información común para el seguimiento de creación y modificación de registros.
    """
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_creados', null=True, blank=True, editable=False)
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    fecha_creacion = models.DateTimeField(default=timezone.now, help_text="Data de creació", editable=False)
    fecha_modificacion = models.DateTimeField(auto_now=True, help_text="Data de modificació", editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)
    

class MetadataModel(models.Model):
    """
    Modelo base para almacenar metadatos utilizados para SEO en las vistas y plantillas.
    """
    metatitulo = models.CharField(max_length=255, help_text="Metatítol per a SEO", null=True, blank=True, verbose_name="Metatítol")
    metadescripcion = models.TextField(help_text="Metadescripció per a SEO", null=True, blank=True, verbose_name="Metadescripció")

    class Meta:
        abstract = True