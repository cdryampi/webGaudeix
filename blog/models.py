from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
from django.db import models

class SubBlog(models.Model):
    titulo = models.CharField(max_length=100, help_text="Título del subblog")
    slug = models.SlugField(unique=True, help_text="Slug del subblog")
    contenido = RichTextField(help_text="Contenido del subblog")
    imagen = models.ImageField(upload_to='blog/subblogs/', help_text="Imagen del subblog")
    color = models.CharField(max_length=7, help_text="Color en formato hexadecimal (ejemplo: #FF0000)")
    link = models.CharField(max_length=200, help_text="Enlace del subblog")
    abrir_en_nueva_ventana = models.BooleanField(default=False, help_text="Abrir enlace en una nueva ventana")
    abrir_en_pespana = models.BooleanField(default=False, help_text="Abrir enlace en la misma ventana con rel='noopener noreferrer'")
    metatitulo = models.CharField(max_length=255, help_text="Metatítulo para SEO")
    metadescripcion = models.TextField(help_text="Metadescripción para SEO")

    def __str__(self):
        return self.titulo


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
    
