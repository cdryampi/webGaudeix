from django.db import models
from core.models import BaseModel, MetadataModel
from ckeditor.fields import RichTextField
from django.utils import timezone
from singleton_model import SingletonModel
from django.contrib.auth import get_user_model
from core.utils import generate_short_slug
from django.utils.text import slugify
from multimedia_manager.models import Fichero
# Create your models here.

class SubvencionDescripcion(MetadataModel, SingletonModel):
    titulo = models.CharField(
        max_length=100,
        help_text="Introdueix el títol.",
    )

    descripcion = RichTextField(
        help_text="Introdueix la descripció.",
    )

    imagen = models.ImageField(upload_to='subvencions',help_text='Selecciona una imatge per a la subvenció.', null=True, blank=True)
    
    disclaimer = RichTextField(
        blank=True,
        help_text="Afegiu qualsevol informació addicional o notes importants aquí.",
    )

    class Meta:
        verbose_name = "Descripció de llistat de les subvencions"
        verbose_name_plural = "Descripció de llistat de les subvencions"
    def __str__(self):
        return self.titulo

class Subvencion(MetadataModel, BaseModel):
    
    titulo = models.CharField(
        max_length=100,
        help_text="Introdueix el títol de la subvenció.",
    )

    descripcion = RichTextField(
        help_text="Introdueix la descripció de la subvenció.",
    )

    disclaimer = RichTextField(
        blank=True,
        help_text="Afegiu qualsevol informació addicional o notes importants aquí.",
    )

    publicado = models.BooleanField(
        default=False, help_text="Indica si el subblog està publicat"
    )
    fecha = models.DateField(default=timezone.now)

    slug = models.SlugField(unique=True, editable=False, max_length=100)
    class Meta:
        verbose_name = "Subvenció"
        verbose_name_plural = "Subvencions"

    def save(self, *args, **kwargs):
        if not self.id:
            # Si es un nuevo objeto, se establece la fecha de creación y el usuario actual
            # Validamos que el campo 'titulo' no esté vacío antes de guardar
            if not self.titulo:
                raise ValueError("El campo 'titulo' no puede estar vacío.")
            self.fecha_creacion = timezone.now()
            self.creado_por = get_user_model().objects.first()
            # Generar un valor hexadecimal único utilizando uuid4
            unique_hex = generate_short_slug()
            self.slug = f"{slugify(self.titulo)}-{unique_hex}"
            
        else:
            
            if not self.creado_por:
                self.creado_por = get_user_model().objects.first()

            self.modificado_por = get_user_model().objects.first()
        # Siempre se actualiza la fecha de modificación y el usuario que modifica
        self.modificado_por = get_user_model().objects.first()
        self.fecha_modificacion = timezone.now()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.titulo


class PDFCollectionConvocatoriaFichero(models.Model):
    titulo = models.CharField(
        max_length=100,
        help_text="Introdueix el títol.",
    )
    
    subvencion = models.ForeignKey(
        Subvencion, on_delete=models.CASCADE, default=None)
    fichero = models.ForeignKey(Fichero, on_delete=models.CASCADE)

    def __str__(self):
        return f"convocatoria: {self.subvencion.titulo} - fichero: {self.fichero}"
    

    def delete(self, *args, **kwargs):
        self.fichero.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = PDFCollectionConvocatoriaFichero.objects.get(pk=self.pk)
            if old_instance.fichero != self.fichero and old_instance.fichero:
                old_instance.fichero.delete()
        super().save(*args, **kwargs)

class PDFCollectionResolucioFichero(models.Model):
    titulo = models.CharField(
        max_length=100,
        help_text="Introdueix el títol.",
    )

    subvencion = models.ForeignKey(
        Subvencion, on_delete=models.CASCADE, default=None)
    fichero = models.ForeignKey(Fichero, on_delete=models.CASCADE)

    def __str__(self):
        return f"convocatoria: {self.subvencion.titulo} - fichero: {self.fichero}"
    

    def delete(self, *args, **kwargs):
        self.fichero.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = PDFCollectionResolucioFichero.objects.get(pk=self.pk)
            if old_instance.fichero != self.fichero and old_instance.fichero:
                old_instance.fichero.delete()
        super().save(*args, **kwargs)

class PDFCollectionJustificacioFichero(models.Model):
    titulo = models.CharField(
        max_length=100,
        help_text="Introdueix el títol.",
    )

    subvencion = models.ForeignKey(
        Subvencion, on_delete=models.CASCADE, default=None)
    fichero = models.ForeignKey(Fichero, on_delete=models.CASCADE)

    def __str__(self):
        return f"convocatoria: {self.subvencion.titulo} - fichero: {self.fichero}"
    

    def delete(self, *args, **kwargs):
        self.fichero.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = PDFCollectionJustificacioFichero.objects.get(pk=self.pk)
            if old_instance.fichero != self.fichero and old_instance.fichero:
                old_instance.fichero.delete()
        super().save(*args, **kwargs)


class PDFCollectionTotesFichero(models.Model):
    titulo = models.CharField(
        max_length=100,
        help_text="Introdueix el títol.",
    )

    subvencion = models.ForeignKey(
        Subvencion, on_delete=models.CASCADE, default=None)
    fichero = models.ForeignKey(Fichero, on_delete=models.CASCADE)

    def __str__(self):
        return f"convocatoria: {self.subvencion.titulo} - fichero: {self.fichero}"
    

    def delete(self, *args, **kwargs):
        self.fichero.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = PDFCollectionTotesFichero.objects.get(pk=self.pk)
            if old_instance.fichero != self.fichero and old_instance.fichero:
                old_instance.fichero.delete()
        super().save(*args, **kwargs)