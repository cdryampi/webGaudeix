from django.db import models
from core.models import BaseModel, MetadataModel
from blog.models import Tag
from multimedia_manager.models import Imagen
from django.utils import timezone
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
User = get_user_model()

# Create your models here.






class Agenda(BaseModel, MetadataModel):
    titulo = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='eventos/')
    fecha = models.DateField(default=timezone.now())
    hora_inicio = models.TimeField(default=timezone.now().replace(hour=0, minute=0))
    hora_fin = models.TimeField(default=timezone.now().replace(hour=1, minute=0))
    ubicacion = models.CharField(max_length=255)
    descripcion_corta = models.CharField(max_length=255)
    descripcion_larga = RichTextField()
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = "Agenda"
        verbose_name_plural = "Agendas"

    def save(self, *args, **kwargs):
        if not self.id:
            # Si es un nuevo objeto, se establece la fecha de creación y el usuario actual
            self.fecha_creacion = timezone.now()
            self.creado_por = get_user_model().objects.first()
        else:
            if not self.creado_por:
                self.creado_por = get_user_model().objects.first()
        # Siempre se actualiza la fecha de modificación y el usuario que modifica
        self.modificado_por = get_user_model().objects.first()
        self.fecha_modificacion = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
    


class GaleriaAgenda(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, default=None)
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = GaleriaAgenda.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Categoría: {self.agenda.titulo} - Imagen: {self.imagen}"


