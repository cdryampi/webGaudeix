from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from core.models import MetadataModel
from map.models import MapPoint
from django.contrib.auth import get_user_model
from blog.models import Post
from multimedia_manager.models import Imagen, Fichero



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







class Diversidad(MetadataModel):
    titulo = models.CharField(
        max_length=255,
        help_text= "afegeix el titul principal",
        verbose_name= "títul"
    )
    sub_titulo = models.CharField(
        max_length=255,
        help_text= "afegeix un subtitul per la landing de igualtat",
        verbose_name="subtítul",
        null=True,
        blank=True
    )
    logros = models.ManyToManyField(
        Post,
        blank=True,
        help_text="Afegeix els èxits que hem obtingut PE (punt lila o els punts segurs)",
        verbose_name="èxits",
        related_name="logros_diversidad"  # Related name personalizado para la relación logros
    )
    planes = models.ManyToManyField(
        Post,
        blank=True,
        help_text="Afegeix els plans que estem seguint per arribar a la igualtat.",
        verbose_name="plans",
        related_name="planes_diversidad"  # Related name personalizado para la relación planes
    )
    descripcion_auxiliar = RichTextField(
        help_text= "Explica a el pla de igualtat",
        verbose_name= "descripció auxiliar",
        blank= True,
        null= True
    )

    def save(self, *args, **kwargs):
        # Verificar si ya existe una instancia activa
        if Diversidad.objects.exists() and not self.pk:
            raise ValidationError("Ja existeix una instància de Diversitat. No es pot crear una altra.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
    
    def delete(self, *args, **kwargs):
        # Evitar que se elimine la instancia
        pass
    
    class Meta:
        verbose_name = "diversitat"
        verbose_name_plural = "diversitat"

class PDFDiversidadFichero(models.Model):
    titulo = models.CharField(
        max_length=100,
        help_text="Introdueix el títol.",
        verbose_name="títul"
    )
    diversidad = models.ForeignKey(
        Diversidad,
        on_delete=models.CASCADE,
        default=None,
        verbose_name="diversitat"
    )
    fichero = models.ForeignKey(
        Fichero,
        on_delete=models.CASCADE,
        verbose_name= "fitxer"
    )

    def __str__(self):
        return f"diversitat: {self.diversidad.titulo} - fichero: {self.fichero}"
    

    def delete(self, *args, **kwargs):
        self.fichero.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = PDFDiversidadFichero.objects.get(pk=self.pk)
            if old_instance.fichero != self.fichero and old_instance.fichero:
                old_instance.fichero.delete()
        super().save(*args, **kwargs)





class DiversidadImagenBanner(models.Model):
    """
    Modelo que representa a la imagen de un post
    """
    nombre = models.CharField(
        max_length=255,
        help_text= "afegeix el nom de la entitat",
        verbose_name= "nom"
    )
    enlace = models.URLField(
        blank=True,
        null=True,
        help_text="Enllaç a cap el lloc virtual de l'entitat",
        verbose_name="Enllaç de l'entitat"
    )
    diversidad = models.ForeignKey(
        Diversidad,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Entrada del Bloc"
    )
    imagen = models.OneToOneField(
        Imagen,
        on_delete=models.CASCADE,
        verbose_name="Imatge"
    )


    class Meta:
        verbose_name = "Imatge de l'entitat"
        verbose_name_plural = "Imatges de les entitats"
    
    def __str__(self):
        return f"Post: {self.diversidad} - Imagen: {self.imagen}"

    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = DiversidadImagenBanner.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)










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