from django.db import models
from ckeditor.fields import RichTextField
from core.models import MetadataModel, BaseModel
from django.utils import timezone
from multimedia_manager.models import Imagen, Fichero
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
from django.core.validators import MinLengthValidator, RegexValidator
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.utils.text import slugify
from django.contrib.auth import get_user_model


User = get_user_model()

class Tag(models.Model):
    nombre = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.nombre



class SubBlog(MetadataModel, BaseModel):
    titulo = models.CharField(max_length=100, help_text="Títol del subblog")
    slug = models.SlugField(unique=True, editable=False, max_length=100)
    contenido = RichTextField(help_text="Contingut del subblog")
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
            # Verificar si el slug ha cambiado
            if self.slug != slugify(self.titulo):
                base_slug = slugify(self.titulo)
                slug = base_slug
                suffix = 1
                while SubBlog.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{suffix}"
                    suffix += 1
                self.slug = slug

        # Siempre se actualiza la fecha de modificación y el usuario que modifica
        self.modificado_por = get_user_model().objects.first()
        self.fecha_modificacion = timezone.now()

        super().save(*args, **kwargs)
    def view_on_site(self, obj):
        url = obj.get_absolute_url()
        if url:
            return mark_safe(f'<a href="{url}" target="_blank">Veure al lloc</a>')
        return None    
    def get_absolute_url(self):
        return reverse('blog:detalle-subblog', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.titulo



class SubBlogImagen(models.Model):
    subblog = models.OneToOneField(
        SubBlog, on_delete=models.CASCADE, null=True)
    imagen = models.OneToOneField(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"SubBlog: {self.subblog} - Imagen: {self.imagen}"

    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = SubBlogImagen.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)


class Categoria(MetadataModel, BaseModel):

    titulo = models.CharField(max_length=255, help_text="Títol de categoría")
    subtitulo = models.CharField(
        max_length=255, help_text="Subtítol de categoria")
    descripcion = RichTextField(help_text="Descripció de categoría")

    slug = models.SlugField(max_length=255, unique=True, editable=False)

    subblog = models.ForeignKey(
        SubBlog, on_delete=models.SET_NULL, null=True, blank=True)
    ESPECIAL_CHOICES = (
        (False, _('No')),
        (True, _('Sí')),
    )
    especial = models.BooleanField(
        _('Categoría Especial'), choices=ESPECIAL_CHOICES, default=False)
    TIPOS = (
        ('normal', 'normal'),
        ('agenda', 'agenda'),
        ('visitas_guiadas', 'visitas guiadas'),
        # Agrega más tipos según tus necesidades
    )

    tipo = models.CharField(max_length=20, choices=TIPOS, default='normal')

    color = ColorField(default='#FFFFFF')

    publicado = models.BooleanField(default=False,help_text="Indica si la categoria està publicada o no. Si està publicada, es mostrarà en la llista de categories disponibles.")

    def save(self, *args, **kwargs):
        
        if not self.id:
            # Si es un nuevo objeto, se establece la fecha de creación y el usuario actual
            self.fecha_creacion = timezone.now()
            self.creado_por = get_user_model().objects.first()
        else:
            if not self.creado_por:
                self.creado_por = get_user_model().objects.first()
        if not self.slug:
            self.slug = slugify(self.titulo)
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
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = CategoriaBannerImagen.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)





class CategoriaGaleriaImagen(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, default=None)
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"Categoría: {self.categoria.titulo} - Imagen: {self.imagen}"
    

    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = CategoriaGaleriaImagen.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)



class Post(MetadataModel, BaseModel):
    titulo = models.CharField(max_length=200)
    descripcion = RichTextField(help_text="Descripció de Post")
    entradas = models.BooleanField(default=False, help_text="Hi ha entrades?")
    slug = models.SlugField(unique=True, editable=False)
    fecha = models.DateField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    publicado = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generar el slug basado en el título
            self.slug = slugify(self.titulo)
        else:
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                # Si ya existe un Post con el mismo slug, añadir un contador al final del slug
                self.slug = f"{original_slug}-{counter}"
                counter += 1

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
        if self.fecha and self.fecha < timezone.now().date() - timezone.timedelta(weeks=1):
            self.entradas = False
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detalle-post', kwargs={'slug': self.slug})
    

    def __str__(self):
        return self.titulo


class PostImagen(models.Model):
    post = models.OneToOneField(
        Post, on_delete=models.CASCADE, null=True)
    imagen = models.OneToOneField(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post: {self.post} - Imagen: {self.imagen}"

    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = PostImagen.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)



class PostGaleriaImagen(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, default=None)
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post: {self.post.titulo} - Imagen: {self.imagen}"
    
    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = PostImagen.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)


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



