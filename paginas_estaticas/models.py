from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from core.models import MetadataModel
from map.models import MapPoint
from django.contrib.auth import get_user_model

User = get_user_model()

class SingletonModel(MetadataModel):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Verificar si ya existe una instancia con el mismo tipo
        existing_instance = self.__class__.objects.first()
        if existing_instance and existing_instance != self:
            raise ValidationError(f"Ya existe una instancia de {self.__class__.__name__}.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass


class PaginaLegal(models.Model):
    TIPOS = (
        ('privacitat', 'Política de privacitat'),
        ('avis_legal', 'Avís legal'),
        ('cookies', 'Política de cookies'),
    )

    tipo = models.CharField(max_length=20, choices=TIPOS, unique=True)
    titulo = models.CharField(max_length=255)
    encabezado = models.CharField(max_length=200) # Campo para el encabezado de la página
    imagen = models.ImageField(upload_to='legal_images/', null=True, blank=True) # Campo para la imagen asociada a la página
    contenido = RichTextField()
    # Otros campos necesarios para tu modelo
    def clean(self):
        # Verificar si ya existe una instancia con el mismo tipo
        if PaginaLegal.objects.exclude(pk=self.pk).filter(tipo=self.tipo).exists():
            raise ValidationError("Ya existe una instancia con el mismo tipo.")
        
    def __str__(self):
        return self.titulo

class PaginaEstatica(SingletonModel):
    pass




class PuntoInformacion(PaginaEstatica):
    telefono = models.CharField(
        max_length=20,
        help_text="Telèfon de contacte",
        verbose_name="Telèfon de contacte"
    )
    titulo = models.CharField(
        max_length=255,
        verbose_name="Títol",
        default="Títol per defecte"
    )
    correo = models.EmailField(
        help_text="Correu electrònic de contacte",
        verbose_name="Correu electrònic de contacte"
    )
    direccion = models.CharField(
        max_length=255,
        help_text="Adreça",
        verbose_name="Adreça"
    )
    banner = models.ImageField(
        upload_to='punto_informacion_banners',
        help_text="Banner del punt d'informació",
        verbose_name="Banner del punt d'informació"
    )
    descripcion = RichTextField(
        help_text="Descripció del punt d'informació",
        verbose_name="Descripció del punt d'informació"
    )
    mapa = models.ForeignKey(
        MapPoint,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Mapa"
    )

    def clean(self):
        if PuntoInformacion.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Només pot existir un objecte de tipus PuntoInformacion")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
    
class Contacto(PaginaEstatica):
    # Atributos específicos del contacto
    titulo = models.CharField(
        max_length=255,
        verbose_name="Títol",
        default="Títol per defecte"
    )
    banner = models.ImageField(
        upload_to='contacto/',
        null=True,
        blank=True,
        help_text="Banner del contacto",
        verbose_name="Banner del contacto"
    )
    subtitulo = models.CharField(
        max_length=100,
        blank=True,
        help_text="Subtítulo del contacto",
        verbose_name="Subtítol del contacto"
    )
    descripcion = RichTextField(
        help_text="Descripción del contacto",
        verbose_name="Descripció del contacte"
    )

    def clean(self):
        if Contacto.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Solo puede existir un objeto de tipo Contacto")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class Cookies(SingletonModel):
    titulo = models.CharField(
        max_length=100,
        help_text="Título de la política de cookies",
        verbose_name="Títol de la política de cookies"
    )
    contenido = models.TextField(
        help_text="Contenido de la política de cookies",
        verbose_name="Contingut de la política de cookies"
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Políticas de Cookies"