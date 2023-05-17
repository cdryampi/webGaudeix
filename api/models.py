from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class TeenvioManager(models.Manager):

    def get_singleton(self):
        # Verificar si ya existe una instancia de Teenvio
        if self.exists():
            # Si existe, retornar la primera instancia encontrada
            return self.first()
        
        # Si no existe, crear una nueva instancia de Teenvio y guardarla
        teenvio = self.create()
        return teenvio
    def create(self, **kwargs):
        # Verificar si ya existe una instancia de Teenvio
        if self.exists():
            raise ValueError("Ya existe una instancia de Teenvio")

        return super().create(**kwargs)


class Teenvio(models.Model):
    # clase que representa las credenciales de Teenvio
    gid = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    plan = models.CharField(max_length=100)
    url = models.URLField(default="https://master5.teenvio.com/v4/public/api/v3/post/")
    subscribers = models.ManyToManyField('Subscriptor', related_name='newsletters')
    objects = TeenvioManager()

    class Meta:
        verbose_name = "API Teenvio"
        verbose_name_plural = "API Teenvio"

    def __str__(self):
        return "API Teenvio"
    
    def save(self, *args, **kwargs):
        if Teenvio.objects.exists():
            # Si ya existe una instancia de Teenvio, no se guarda una nueva
            raise ValidationError("Ya existe una instancia de Teenvio.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Evitar borrar la instancia de Teenvio
        pass
class Subscriptor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    exportable = models.BooleanField(default=True)
    # Otros campos relevantes para los subscriptores
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name
