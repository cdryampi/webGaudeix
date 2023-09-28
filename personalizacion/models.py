from django.db import models
from django.core.exceptions import ValidationError
from blog.models import Post, Categoria, SubBlog, Tag
from multimedia_manager.models import Video
from topbar.models import Topbar

from .utils import get_parallax_image_path


# Create your models here.
class PersonalizacionManager(models.Manager):
    def get_singleton(self):
        # Verificar si ya existe una instancia de Personalizacion
        if self.exists():
            # Si existe, retornar la primera instancia encontrada
            return self.first()

        # Si no existe, crear una nueva instancia de Personalizacion y guardarla
        personalizacion = self.create()
        return personalizacion




class Favicon(models.Model):
    image = models.ImageField(upload_to='favicons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favicon"
        verbose_name_plural = "Favicons"

    def __str__(self):
        return f"Favicon {self.id}"

    @property
    def description(self):
        return "Este favicon se utiliza como icono de la pestaña del navegador para identificar tu sitio web."






class Slide(models.Model):
    imagen = models.ImageField(upload_to='slides/')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=100,help_text="Texto que aparecerá en el centro del carrusel", null=True, blank=True)
    def __str__(self):
        return self.titulo



class InternalLink(models.Model):
    TIPOS_REFERENCIA = (
        ('post', 'Post'),
        ('categoria', 'Categoría'),
        ('subblog', 'SubBlog')
    )

    tipo = models.CharField(max_length=10, choices=TIPOS_REFERENCIA)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
    subblog = models.ForeignKey(SubBlog, on_delete=models.CASCADE, blank=True, null=True)
    slide = models.OneToOneField(Slide, on_delete=models.CASCADE)
    
    def __str__(self):
        tipo = self.get_tipo_display()
        titulo = ""

        # Comprueba cada atributo en el orden deseado para encontrar el título
        if self.post:
            titulo = self.post.titulo
        elif self.categoria:
            titulo = self.categoria.titulo
        elif self.subblog:
            titulo = self.subblog.titulo

        return f"{tipo}: {titulo}"


    def save(self, *args, **kwargs):
        if self.tipo == 'post':
            self.categoria = None
            self.subblog = None
        elif self.tipo == 'categoria':
            self.post = None
            self.subblog = None
        elif self.tipo == 'subblog':
            self.post = None
            self.categoria = None


        super().save(*args, **kwargs)




class Carrusel(models.Model):
    nombre = models.CharField(max_length=100)
    publicado = models.BooleanField(default=False)
    slides = models.ManyToManyField(Slide, related_name='carruseles', blank=True)

    class Meta:
        verbose_name = 'Carrusel'
        verbose_name_plural = 'Carruseles'

    def __str__(self):
        return self.nombre



class Parallax(models.Model):
    
    titulo = models.CharField(max_length=100)
    descripcion_corta = models.CharField(max_length=200, null= True, blank= True)
    imagen = models.ImageField(upload_to=get_parallax_image_path)
    publicado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo



class VideosEmbed(models.Model):
    titulo = models.CharField(
        max_length=100,
    )
    publicado = models.BooleanField(default=False)
    video = models.OneToOneField(Video, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"Portada de video: {self.titulo}"


class Personalizacion(models.Model):
    # modelo que representa la personalización del sitio.

    favicon = models.OneToOneField(
        Favicon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Favicon",
        help_text="Selecciona el favicon per al lloc (si n'hi ha un)."
    )
    parallax_portada = models.OneToOneField(
        Parallax,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Parallax de portada",
        help_text="Selecciona el parallax per a la portada (si n'hi ha un)."
    )
    video_portada = models.OneToOneField(
        Video,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Vídeo de portada",
        help_text="Selecciona el vídeo per a la portada (si n'hi ha un)."
    )
    topbar = models.OneToOneField(
        Topbar,
        on_delete= models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Topbar del portal",
        help_text= "Selecciona el topbar que vols per la portada"
    )
    analytics_script = models.TextField(
        null=True,
        blank=True,
        verbose_name="Script de Google Analytics",
        help_text="Col·loca aquí el teu codi de Google Analytics."
    )
    meta_description_portada = models.TextField(
        null=True,
        blank=True,
        verbose_name="Meta descripció de portada",
        help_text="Especifica una descripció meta per a la portada del lloc."
    )
    meta_keywords = models.ManyToManyField(
        Tag,
        verbose_name="Paraules clau meta",
        help_text="Selecciona les paraules clau meta relacionades amb el lloc.",
        blank=True,
    )
    objects = PersonalizacionManager()

    class Meta:
        verbose_name = "Personalització"
        verbose_name_plural = "Personalitzacions"
    def __str__(self):
        return "Personalització del portal"
    
    def save(self, *args, **kwargs):
        # Solo se permite guardar una única instancia de Personalizacion
        if Personalizacion.objects.exists() and not self.pk:
            raise ValueError("Ya existe una instancia de Personalizacion. No se puede crear otra.")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # No se permite eliminar la instancia de Personalizacion
        raise ValueError("No se puede eliminar la instancia de Personalizacion.")

