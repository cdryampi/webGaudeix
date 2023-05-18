from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BaseModel(models.Model):
    
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_creados', null=True, blank=True, editable=False)
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    fecha_creacion = models.DateTimeField(default=timezone.now, help_text="Fecha de creación", editable=False)
    fecha_modificacion = models.DateTimeField(auto_now=True, help_text="Fecha de modificación", editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)
    

class MetadataModel(models.Model):
    metatitulo = models.CharField(max_length=255, help_text="Metatítulo para SEO", null=True, blank=True)
    metadescripcion = models.TextField(help_text="Metadescripción para SEO", null=True, blank=True)

    class Meta:
        abstract = True