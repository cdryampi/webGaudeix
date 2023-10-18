from django.db import models
from django.core.exceptions import ValidationError
from blog.models import Post, Categoria, SubBlog, Tag
from multimedia_manager.models import Video
from topbar.models import Topbar
from ckeditor.fields import RichTextField
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
    image = models.ImageField(
        upload_to='favicons/',
        blank=True,
        null=True,
        verbose_name="Imatge"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favicon"
        verbose_name_plural = "Favicons"

    def __str__(self):
        return f"Favicon {self.id}"

    @property
    def description(self):
        return "Aquest Favicon el sistema el fa servir per a la imatge representativa del lloc web."






class Slide(models.Model):
    imagen = models.ImageField(
        upload_to='slides/',
        verbose_name="Imatge"
    )
    titulo = models.CharField(
        max_length=100,
        verbose_name='Títol'
    )
    descripcion = models.TextField(
        max_length=100,
        help_text="Text que apareix el centre de la imatge.",
        null=True,
        blank=True
    )
    def __str__(self):
        return self.titulo



class InternalLink(models.Model):
    TIPOS_REFERENCIA = (
        ('post', 'Post'),
        ('categoria', 'Categoría'),
        ('subblog', 'SubBlog')
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPOS_REFERENCIA,
        verbose_name="Tipus"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="entrada"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Categoría"
    )
    subblog = models.ForeignKey(
        SubBlog,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    slide = models.OneToOneField(
        Slide,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        tipo = self.tipo
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
    nombre = models.CharField(
        max_length=100,
        verbose_name="Títol"
    )
    publicado = models.BooleanField(
        default=False,
        verbose_name="Publicat"
    )
    slides = models.ManyToManyField(
        Slide,
        related_name='carruseles',
        blank=True
    )

    class Meta:
        verbose_name = 'Carrusel'
        verbose_name_plural = 'Carrusels'

    def __str__(self):
        return self.nombre



class Parallax(models.Model):
    
    titulo = models.CharField(
        max_length=100,
        verbose_name="Títol"
    )
    descripcion_corta = models.CharField(
        max_length=200,
        null= True,
        blank= True,
        verbose_name="Descripció curta"
    )
    imagen = models.ImageField(
        upload_to=get_parallax_image_path,
        verbose_name="Imatge"
    )
    publicado = models.BooleanField(
        default=False,
        verbose_name="Publicat"
    )

    def __str__(self):
        return self.titulo



class VideosEmbed(models.Model):
    titulo = models.CharField(
        max_length=100,
        help_text="Títol del Vídeo.",
        verbose_name="Títol"
    )
    publicado = models.BooleanField(
        default=False,
        verbose_name="Publicat"
    )
    video = models.OneToOneField(Video, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"Portada de video: {self.titulo}"



class AgendaParallax(models.Model):
    """
        Modelo que representa la imagen de la agenda.
    """
    
    titulo = models.CharField(
        max_length=100,
        help_text="Títol del parallax.",
        verbose_name="Títol"
    )
    parallax_agenda = models.OneToOneField(
        Parallax,
        on_delete=models.CASCADE,
        verbose_name="Parallax de l'agenda",
        help_text="Selecciona el parallax per a l'agenda (si n'hi ha un)."
    )

    def __str__(self):
        return f"Parallax {self.titulo}"

    class Meta:
        verbose_name = "Imatge per l'agenda"
        verbose_name_plural = "Imatges per l'agenda"


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
    parallax_agenda = models.OneToOneField(
        AgendaParallax,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Parallax de l'agenda",
        help_text="Selecciona el parallax per l'agenda (si n'hi ha un)."
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






class TrenPersonalizacion(models.Model):
    """
    Modelo que representa un modo de llegar a Cabrera de Mar por tren.
    """
    titulo = models.CharField(
        max_length=100,
        help_text="Títol de 'com arribar a Cabrera amb tren'.",
        verbose_name="Títol"
    )
    
    descripcion = RichTextField(
        help_text="Descripció de com arribar a Cabrera de Mar amb tren.",
        null=True,
        blank=True,
        verbose_name="Descripció"
    )

    enlace =  models.URLField(
        blank=True,
        help_text="enllaç cap a els horaris del tren",
        verbose_name="enllaç"
    )

    personalizacion = models.OneToOneField(
        Personalizacion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Personalització",
    )

    def __str__(self):
        return f"{self.titulo}"
    
    class Meta:
        verbose_name = "Tren"
        verbose_name_plural = "Trens"

class AutoPistaPersonalizacion(models.Model):
    """
    Modelo que representa un modo de llegar a Cabrera de Mar por Autopista.
    """

    titulo = models.CharField(
        max_length=100,
        help_text="Títol de 'com arribar a Cabrera per autopista'.",
        verbose_name="Títol"
    )
    descripcion = RichTextField(
        help_text="Explicació de com arribar a Cabrera de Mar per autopista.",
        null=True,
        blank=True,
        verbose_name="Descripció"
    )
    enlace = models.URLField(
        blank= True,
        help_text="enllaç cap a Cabrera de Mar.",
        verbose_name="enllaç"
    )
    personalizacion = models.OneToOneField(
        Personalizacion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Personalització",
    )

    def __str__(self):
        return f"{self.titulo}"
    
    class Meta:
        verbose_name = "Autopista"
        verbose_name_plural = "Autopistes"

class BusPersonalizacion(models.Model):
    """
    Modelo que representa un modo de llegar a Cabrera de Mar por bus.
    """
    titulo = models.CharField(
        max_length=100,
        help_text="Títol de 'com arribar a Cabrera de Mar amb bus'.",
        verbose_name="Títol"
    )
    descripcion = RichTextField(
        help_text="Explicació de com arribar a Cabrera de Mar amb bus.",
        null=True,
        blank=True,
        verbose_name="Descripció"
    )
    enlace = models.URLField(
        blank= True,
        help_text="enllaç cap els horaris del bus.",
        verbose_name="enllaç"
    )
    personalizacion = models.OneToOneField(
        Personalizacion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Personalització",
    )

    def __str__(self):
        return f"{self.titulo}"
    
    class Meta:
        verbose_name = "Bus"
        verbose_name_plural = "Busos"

class AeropuertoPersonalizacion(models.Model):
    """
    Modelo que representa un modo de llegar a Cabrera de Mar por Avión.
    """
    titulo = models.CharField(
        max_length=100,
        help_text="Títol de 'com arribar a Cabrera de Mar amb avió'.",
        verbose_name="Títol"
    )
    descripcion = RichTextField(
        help_text="Explicació de com arribar a Cabrera de Mar amb avió.",
        null=True,
        blank=True,
        verbose_name="Descripció"
    )
    enlace_principal = models.URLField(
        blank= True,
        help_text="enllaç cap els horaris del bus.",
        verbose_name="enllaç principal"
    )
    enlace_secundario = models.URLField(
        blank= True,
        help_text="enllaç cap els horaris del bus.",
        verbose_name="enllaç secundari"
    )
    personalizacion = models.OneToOneField(
        Personalizacion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Personalització",
    )

    def __str__(self):
        return f"{self.titulo}"
    
    class Meta:
        verbose_name = "Aeroport"
        verbose_name_plural = "Aeroports"