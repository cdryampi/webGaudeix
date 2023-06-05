from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from core.models import MetadataModel
from django.contrib.auth import get_user_model

User = get_user_model()

class SingletonModel(MetadataModel):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

class PaginaEstatica(SingletonModel):
    titulo = models.CharField(max_length=255)

    def __str__(self):
        return self.titulo

class Agenda(PaginaEstatica):
    banner = models.ImageField(upload_to='agenda_banners')
    # otros campos específicos de la agenda

class PuntoInformacion(PaginaEstatica):
    telefono = models.CharField(max_length=20, help_text="Telèfon de contacte")
    correo = models.EmailField(help_text="Correu electrònic de contacte")
    direccion = models.CharField(max_length=255, help_text="Adreça")
    banner = models.ImageField(upload_to='punto_informacion_banners', help_text="Banner del punt d'informació")
    descripcion = RichTextField(help_text="Descripció del punt d'informació")
    latitud = models.FloatField(help_text="Latitud per a Google Maps")
    longitud = models.FloatField(help_text="Longitud per a Google Maps")

    def clean(self):
        if PuntoInformacion.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Només pot existir un objecte de tipus PuntoInformacion")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

class Contacto(PaginaEstatica):
    # Atributos específicos del contacto
    banner = models.ImageField(upload_to='contacto/', null=True, blank=True, help_text="Banner del contacto")
    subtitulo = models.CharField(max_length=100, blank=True, help_text="Subtítulo del contacto")
    descripcion = models.TextField(blank=True, help_text="Descripción del contacto")

    def clean(self):
        if Contacto.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Solo puede existir un objeto de tipo Contacto")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)