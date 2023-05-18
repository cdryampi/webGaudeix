from django.db import models
from ckeditor.fields import RichTextField
from core.models import MetadataModel, BaseModel
from django.utils import timezone
from multimedia_manager.models import Imagen
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()




class SubBlog(MetadataModel, BaseModel):
    titulo = models.CharField(max_length=100, help_text="Título del subblog")
    slug = models.SlugField(unique=True, editable=False, max_length=100)
    contenido = models.TextField(help_text="Contenido del subblog")
    publicado = models.BooleanField(default=False, help_text="Indica si el subblog está publicado")

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



class SubBlogImagen(models.Model):
    subblog = models.OneToOneField(SubBlog, on_delete=models.CASCADE)
    imagen = models.OneToOneField(Imagen, on_delete=models.CASCADE)

    def __str__(self):
        return f"SubBlog: {self.subblog} - Imagen: {self.imagen}"



class Categoria(models.Model):
    titulo = models.CharField(max_length=255)
    subtitulo = models.CharField(max_length=255)
    descripcion = RichTextField()
    imagen_principal = models.ImageField(upload_to='categoria/imagenes/', null=True, blank=True)
    meta_titulo = models.CharField(max_length=255, blank=True)
    meta_descripcion = models.TextField(blank=True)
    subblog = models.ForeignKey(SubBlog, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.titulo



class Post(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen_interior = models.ImageField(upload_to='blog/imagenes/')
    color = models.CharField(max_length=7)
    meta_titulo = models.CharField(max_length=200)
    meta_descripcion = models.TextField()
    fecha = models.DateField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo



class GaleriaImagen(models.Model):
    # modelo que reprenta una Galería de fotos Categoría
    imagen = models.ImageField(upload_to='categoria/galeria/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='imagenes', default=1)

class GaleriaImagenPost(models.Model):
    # modelo que representa una Galería de fotos de un Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='galeria_imagenes', default=1)
    imagen = models.ImageField(upload_to='blog/galerias/')

    def __str__(self):
        return self.imagen.name


class Fichero(models.Model):
    # modelo que representa un Fichero de Categoría
    archivo = models.FileField(upload_to='categoria/ficheros/')
    categoria = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ficheros', default=1)
    
