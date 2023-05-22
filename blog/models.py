from django.db import models
from ckeditor.fields import RichTextField
from core.models import MetadataModel, BaseModel
from django.utils import timezone
from multimedia_manager.models import Imagen, Fichero

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
from django.core.validators import MinLengthValidator, RegexValidator

from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class SubBlog(MetadataModel, BaseModel):
    titulo = models.CharField(max_length=100, help_text="Títol del subblog")
    slug = models.SlugField(unique=True, editable=False, max_length=100)
    contenido = models.TextField(help_text="Contingut del subblog")
    publicado = models.BooleanField(
        default=False, help_text="Indica si el subblog està publicat")

    def save(self, *args, **kwargs):
        if not self.id:
            # Si es un nuevo objeto, se establece la fecha de creación y el usuario actual
            self.fecha_creacion = timezone.now()
            self.creado_por = get_user_model().objects.first()
            self.slug = slugify(self.titulo)
        else:
            if not self.creado_por:
                self.creado_por = get_user_model().objects.first()
        # Siempre se actualiza la fecha de modificación y el usuario que modifica
        self.modificado_por = get_user_model().objects.first()
        self.fecha_modificacion = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class SubBlogImagen(models.Model):
    subblog = models.OneToOneField(
        SubBlog, on_delete=models.CASCADE, null=True)
    imagen = models.OneToOneField(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"SubBlog: {self.subblog} - Imagen: {self.imagen}"

    def delete(self, *args, **kwargs):
        # Eliminar la imagen asociada antes de eliminar el objeto SubBlogImagen
        self.imagen.delete()
        super().delete(*args, **kwargs)


class Categoria(MetadataModel, BaseModel):

    titulo = models.CharField(max_length=255, help_text="Títol de categoría")
    subtitulo = models.CharField(
        max_length=255, help_text="Subtítol de categoria")
    descripcion = RichTextField(help_text="Descripció de categoría")
    subblog = models.ForeignKey(
        SubBlog, on_delete=models.SET_NULL, null=True, blank=True)
    ESPECIAL_CHOICES = (
        (False, _('No')),
        (True, _('Sí')),
    )
    especial = models.BooleanField(
        _('Categoría Especial'), choices=ESPECIAL_CHOICES, default=False)
    color = ColorField(default='#FFFFFF')

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


class CategoriaBannerImagen(models.Model):
    categoria = models.OneToOneField(Categoria, on_delete=models.CASCADE,null=True)
    imagen = models.OneToOneField(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"Categoria: {self.categoria} - Imagen: {self.imagen}"

    def delete(self, *args, **kwargs):
        # Eliminar la imagen asociada antes de eliminar el objeto CategoriaBannerImagen
        self.imagen.delete()
        super().delete(*args, **kwargs)





class CategoriaGaleriaImagen(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, default=None)
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"Categoría: {self.categoria.titulo} - Imagen: {self.imagen}"


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    color = models.CharField(max_length=7)
    meta_titulo = models.CharField(max_length=200)
    meta_descripcion = models.TextField()
    fecha = models.DateField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class PostImagen(models.Model):
    post = models.OneToOneField(
        Post, on_delete=models.CASCADE, null=True)
    imagen = models.OneToOneField(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post: {self.post} - Imagen: {self.imagen}"

    def delete(self, *args, **kwargs):
        # Eliminar la imagen asociada antes de eliminar el objeto SubBlogImagen
        self.imagen.delete()
        super().delete(*args, **kwargs)



class PostGaleriaImagen(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, default=None)
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post: {self.post.titulo} - Imagen: {self.imagen}"


class PostFichero(models.Model):
    post = models.OneToOneField(
        Post, on_delete=models.CASCADE, null=True)
    fichero = models.OneToOneField(Fichero, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post: {self.post} - Fichero: {self.fichero}"

    def delete(self, *args, **kwargs):
        # Eliminar la imagen asociada antes de eliminar el objeto SubBlogImagen
        self.imagen.delete()
        super().delete(*args, **kwargs)
