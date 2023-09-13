from django.db import models
from ckeditor.fields import RichTextField
from core.models import MetadataModel, BaseModel
from django.utils import timezone
from multimedia_manager.models import Imagen, Fichero
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
from django.core.validators import MinLengthValidator, RegexValidator, MaxLengthValidator
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.utils.text import slugify
from django.contrib.auth import get_user_model
from core.utils import generate_short_slug


User = get_user_model()

class Tag(models.Model):
    """
    Modelo para representar etiquetas asociadas a las entradas de tipo Agenda principalmente del blog.
    """
    nombre = models.CharField(
        max_length=255,
        validators=
            [MaxLengthValidator(255)],  # Agregar validador de longitud máxima
            help_text="Títol del tag",
            verbose_name="Nom"
        )

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetes"

    def __str__(self):
        return self.nombre



class SubBlog(MetadataModel, BaseModel):
    """
    Modelo para representar subblogs en el sitio web.
    """
    titulo = models.CharField(
        max_length=100,
        help_text="Títol del subblog",
        verbose_name="Títol"
    )
    slug = models.SlugField(
        unique=True,
        editable=False,
        max_length=100
    )
    contenido = RichTextField(
        help_text="Contingut del subblog",
        verbose_name="Contingut"
    )
    publicado = models.BooleanField(
        default=False,
        help_text="Indica si el subblog està publicat",
        verbose_name="Publicat"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="Tags"
    )

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
            self.slug = f"{slugify(self.titulo)[:44]}-{unique_hex}"
        else:
            # Obtener el título anterior del objeto si existe
            old_instance = self.__class__.objects.get(pk=self.pk)
            old_titulo = old_instance.titulo if old_instance else None

            if self.titulo != old_titulo:
                unique_hex = generate_short_slug()
                self.slug = f"{slugify(self.titulo)[:44]}-{unique_hex}"

            if not self.creado_por:
                self.creado_por = get_user_model().objects.first()

            self.modificado_por = get_user_model().objects.first()
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
    """
    Modelo para asociar una imagen a un subblog.
    """
    subblog = models.OneToOneField(
        SubBlog,
        on_delete=models.CASCADE, null=True,
        verbose_name="SubBlog"
    )
    imagen = models.OneToOneField(
        Imagen,
        on_delete=models.CASCADE,
        verbose_name="Imatge"
    )

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

class SubblogGaleriaImagen(models.Model):
    """
    Modelo para asociar una imagen de galería a un subblog.
    """
    subblog = models.ForeignKey(
        SubBlog,
        on_delete=models.CASCADE,
        default=None,
        verbose_name="SubBlog"
    )
    imagen = models.ForeignKey(
        Imagen,
        on_delete=models.CASCADE,
        verbose_name="Imatge de la Galeria"
    )

    def __str__(self):
        return f"Subblog: {self.subblog.titulo} - Imagen: {self.imagen}"
    

    def delete(self, *args, **kwargs):
        self.imagen.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se cambia la imagen
        if self.pk:
            old_instance = SubblogGaleriaImagen.objects.get(pk=self.pk)
            if old_instance.imagen != self.imagen and old_instance.imagen:
                old_instance.imagen.delete()
        super().save(*args, **kwargs)


class Categoria(MetadataModel, BaseModel):
    """
    Modelo que representa una categoría de organización de contenido. Puede ser asignada a diferentes tipos de contenido como Posts, Agendas, etc.
    """
    titulo = models.CharField(
        max_length=255,
        help_text="Títol de categoría",
        verbose_name="Títol"
    )
    subtitulo = models.CharField(
        max_length=255,
        help_text="Subtítol de categoria",
        verbose_name="Subtítol"
    )
    descripcion = RichTextField(
        help_text="Descripció de categoría",
        verbose_name="Descripció"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        editable=False
    )
    subblog = models.ForeignKey(
        SubBlog,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Subblog"
    )
    ESPECIAL_CHOICES = (
        (False, _('No')),
        (True, _('Sí')),
    )
    especial = models.BooleanField(
        choices=ESPECIAL_CHOICES,
        default=False,
        verbose_name="Categoria Especial"
    )
    TIPOS = (
        ('normal', 'normal'),
        ('agenda', 'agenda'),
        ('visitas_guiadas', 'visitas guiadas'),
        ('senderisme','senderisme'),
        ('noticies','noticies'),
        ('lloc','lloc'),
        ('festes_i_tradicions','festes i tradicions')
        
        # Agrega más tipos según tus necesidades
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPOS,
        default='normal',
        verbose_name="Tipus"
    )
    color = ColorField(
        default='#FFFFFF'
    )
    publicado = models.BooleanField(
        default=False,
        help_text="Indica si la categoria està publicada o no. Si està publicada, es mostrarà en la llista de categories disponibles.",
        verbose_name="Publicat"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="Tags"
    )

    def save(self, *args, **kwargs):
        
        if not self.id:
            # Si es un nuevo objeto, se establece la fecha de creación y el usuario actual
            self.fecha_creacion = timezone.now()
            self.creado_por = get_user_model().objects.first()
            # Generar un valor hexadecimal único utilizando uuid4
            unique_hex = generate_short_slug()
            self.slug = f"{slugify(self.titulo)[:44]}-{unique_hex}"
        else:
            # Obtener el título anterior del objeto si existe
            old_instance = self.__class__.objects.get(pk=self.pk)
            old_titulo = old_instance.titulo if old_instance else None

            if self.titulo != old_titulo:
                unique_hex = generate_short_slug()
                self.slug = f"{slugify(self.titulo)[:44]}-{unique_hex}"

            if not self.creado_por:
                self.creado_por = get_user_model().objects.first()

        if not self.slug:
            self.slug = f"{slugify(self.titulo)[:44]}-{unique_hex}"
        # Siempre se actualiza la fecha de modificación y el usuario que modifica
        self.modificado_por = get_user_model().objects.first()
        self.fecha_modificacion = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categories"

class CategoriaBannerImagen(models.Model):
    """
    Descripció de la classe CategoriaBannerImagen:
    Aquest model representa les imatges de banner associades a les categories especials.
    """
    categoria = models.OneToOneField(
        Categoria,
        on_delete=models.CASCADE,
        null=True, 
        verbose_name="Categoria"
    )
    imagen = models.OneToOneField(
        Imagen,
        on_delete=models.CASCADE,
        verbose_name="Imatge del Banner"
    )

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

    class Meta:
        verbose_name = "Imatge de Banner de Categoria"
        verbose_name_plural = "Imatges de Banner de Categoria"



class CategoriaGaleriaImagen(models.Model):
    """
    Representa imágenes de galería asociadas a categorías, usadas para generar miniaturas de contenido relacionado.
    Se eliminan automáticamente junto a la categoría.
    """
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        default=None,
        verbose_name="Categoria"
    )
    imagen = models.ForeignKey(
        Imagen,
        on_delete=models.CASCADE,
        verbose_name="Imatge de la Galeria"
    )

    class Meta:
        verbose_name = "Imatge de Galeria de Categoria"
        verbose_name_plural = "Imatges de Galeria de Categoria"
    
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
    """
    Representa una entrada del blog con título, descripción, categoría y etiquetas.
    La plantilla asociada se define según el tipo de categoría elegido, permitiendo una presentación personalizada en el sitio web.
    """
    titulo = models.CharField(
        max_length=200,
        help_text="Aquest camp està limitat per un màxim de 50 caràcters",
        verbose_name="Títol"
    )
    descripcion = RichTextField(
        help_text="Descripció de Post",
        verbose_name="Descripció"
    )
    slug = models.SlugField(
        unique=True,
        editable=False
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        verbose_name="Categoria"
    )
    publicado = models.BooleanField(
        default=False,
        verbose_name="Publicat"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="Tags"
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generar el slug basado en el título
            # Generar un valor hexadecimal único utilizando uuid4
            unique_hex = generate_short_slug()
            self.slug = f"{slugify(self.titulo)[:44]}-{unique_hex}"

        if not self.id:
            # Si es un nuevo objeto, se establece la fecha de creación y el usuario actual
            self.fecha_creacion = timezone.now()
            self.creado_por = get_user_model().objects.first()
        else:
            # Obtener el título anterior del objeto si existe
            old_instance = self.__class__.objects.get(pk=self.pk)
            old_titulo = old_instance.titulo if old_instance else None

            if self.titulo != old_titulo:
                unique_hex = generate_short_slug()
                self.slug = f"{slugify(self.titulo)[:44]}-{unique_hex}"
            if not self.creado_por:
                self.creado_por = get_user_model().objects.first()
        # Siempre se actualiza la fecha de modificación y el usuario que modifica
        self.modificado_por = get_user_model().objects.first()
        self.fecha_modificacion = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detalle_post', kwargs={'slug': self.slug})
    

    def __str__(self):
        return self.titulo


class PostImagen(models.Model):
    """
    Modelo que representa a la imagen de un post
    """
    post = models.OneToOneField(
        Post,
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
        verbose_name = "Imatge de l'Entrada del Bloc"
        verbose_name_plural = "Imatges de les Entrades del Bloc"
    
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
    """
    Modelo que representa una galería en un Post
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        default=None,
        verbose_name="Entrada del Bloc"
    )
    imagen = models.ForeignKey(
        Imagen,
        on_delete=models.CASCADE,
        verbose_name="Imatge"
    )

    class Meta:
        verbose_name = "Galeria d'Imatges de l'Entrada del Bloc"
        verbose_name_plural = "Galeria d'Imatges de les Entrades del Bloc"

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
    """
    Model que representa un fitxer associat a una Entrada del Bloc
    """
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Entrada del Bloc"
    )
    fichero = models.OneToOneField(
        Fichero,
        on_delete=models.CASCADE,
        verbose_name="Fitxer"
    )

    def __str__(self):
        return f"Post: {self.post} - Fichero: {self.fichero}"

    def delete(self, *args, **kwargs):
        # Eliminar la imagen asociada antes de eliminar el objeto SubBlogImagen
        self.fichero.delete()
        super().delete(*args, **kwargs)



class Noticia(MetadataModel):
    """
    Modelo que representa una noticia.
    """
    titulo = models.CharField(
        max_length=200,
        help_text="Títol de la notícia",
        verbose_name="Títol"
    )
    slug = models.SlugField(
        unique=True,
        editable=False
    )
    contenido = models.TextField(
        help_text="Contingut de la notícia",
        verbose_name = 'contingut'
    )
    fecha = models.DateField(
        default=timezone.now,
        help_text="Data de la notícia"
    )
    imagen_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Imatge URL"
    )
    categoria = models.ForeignKey(
        'blog.Categoria',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Categoria"
    )
    publicado = models.BooleanField(
        default=False,
        help_text="Indica si la notícia està publicada",
        verbose_name="publicat"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generar el slug basado en el título
            unique_hex = generate_short_slug()
            self.slug = f"{slugify(self.titulo)[:44]}-{unique_hex}"
        else:
            # Obtener el título anterior del objeto si existe
            old_instance = self.__class__.objects.get(pk=self.pk)
            old_titulo = old_instance.titulo if old_instance else None

            if self.titulo != old_titulo:
                unique_hex = generate_short_slug()
                self.slug = f"{slugify(self.titulo)[:44]}-{unique_hex}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícies"