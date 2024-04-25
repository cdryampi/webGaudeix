from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from blog.models import Post, Categoria, SubBlog, Tag
from multimedia_manager.models import Video, Parallax, VideosEmbed, Carrusel
from topbar.models import Topbar
from ckeditor.fields import RichTextField
from compra_y_descubre.models import CompraDescubre
from eventos_especiales.models import EventoEspecial
from alerta.models import Alerta
from datetime import time
from colorfield.fields import ColorField

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


class InternalLink(models.Model):
    TIPOS_REFERENCIA = (
        ('eventos_especiales', 'Esdeveniments especials'),
        ('compra_y_descubre', 'Compra i descobreix')
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_REFERENCIA,
        verbose_name="Tipus"
    )
    evento_especial = models.ForeignKey(
        EventoEspecial,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Esdeveniment especial' 
    )
    compra_y_descubre = models.ForeignKey(
        CompraDescubre,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Compra i descobreix' 
    )

    
    def __str__(self):
        tipo = self.tipo
        titulo = ""

        # Comprueba cada atributo en el orden deseado para encontrar el título
        if self.evento_especial:
            titulo = self.evento_especial.titulo
        elif self.compra_y_descubre:
            titulo = self.compra_y_descubre.titulo

        return f"{tipo}: {titulo}"


    def save(self, *args, **kwargs):

        if self.tipo == 'eventos_especiales':
            self.compra_y_descubre = None
        
        elif self.tipo == 'compra_y_descubre':
            self.evento_especial = None

        
        super().save(*args, **kwargs)


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


class IframeVideoHome(models.Model):
    """
        Clase que representa a un vídeo youtube de la portada
    """
    internal_name = models.CharField(
        max_length=255,
        verbose_name="Nom intern", 
        help_text="Nom intern per identificar el vídeo dins del sistema."
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Títol", 
        help_text="Títol del vídeo que es mostrarà públicament."
    )
    description = models.TextField(
        verbose_name="Descripció",    
        null=True,
        blank=True,
        help_text="Descripció detallada del contingut del vídeo."
    )
    video_url = models.URLField(
        verbose_name="URL del vídeo", 
        help_text="URL de l'iframe del vídeo. Utilitza URLs que respectin la privacitat com 'youtube-nocookie' per a YouTube."
    )

    def __str__(self):
        return self.title



class Personalizacion(models.Model):
    # modelo que representa la personalización del sitio.
    HORARIOS = (
        ('estiu','estiu'),
        ('hivern','hivern')
    )
    horario = models.CharField(
        max_length=20,
        choices=HORARIOS,
        default="estiu",
        verbose_name="Horari",
        help_text="Selecciona el teu horari, serveix principalment per donar suport els components de la web amb el canvi d'horari quan fa falta."
    )
    hora_agenda_fin = models.TimeField(
        default=time(2,0,0),
        verbose_name="temps per defecte dels esdeveniments",
        help_text="Durada dels esdeveniments de l'agenda."

    )
    favicon = models.OneToOneField(
        Favicon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Favicon",
        help_text="Selecciona el favicon per al lloc (si n'hi ha un)."
    )
    alerta = models.OneToOneField(
        Alerta,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Alerta",
        help_text="Selecciona una Alerta per la portada."
    )
    carrusel_portada = models.ForeignKey(
        Carrusel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Carrusel de portada",
        help_text="Selecciona el carrusel per a la portada (si n'hi ha un).",
        related_name='personalizaciones_portada'
    )
    carrusel_agenda = models.ForeignKey(
        Carrusel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Carrusel-collage de portada",
        help_text="Selecciona el carrusel-collage per a la agenda (si n'hi ha un).",
        related_name='personalizaciones_agenda'
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

    dias_vista_agenda = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        verbose_name="Dies pel PDF de l'agenda.",
        help_text="Defineix el nombre de dies per generar el PDF de l'agenda, des de 0 fins a 30."
    )
    enlace_agenda = models.URLField(
        blank=True,
        null=True,
        help_text="Enllaç per comprar tiquets per l'agenda",
        verbose_name="enllaç pels tiquets"
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
    video_url = models.OneToOneField(
        IframeVideoHome,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Vídeo auxiliar per la portada",
        help_text="Selecciona el vídeo auxiliar per a la portada (si n'hi ha un)."
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



class SuperDestacado(models.Model):
    """
        Modelo que representa a un super destacado
    """
    titulo = models.CharField(
        max_length=100,
        help_text="Títol del super destacat.",
        verbose_name="Títol"
    )
    descripcion = models.TextField(
        help_text="Títol que sortirà com a encapçalament al superdestacat.",
        null=True,
        blank=True,
        verbose_name="Descripció"
    )
    destacado = models.OneToOneField(
        InternalLink,
        on_delete=models.CASCADE,
        verbose_name="Destacat",
        help_text="Selecciona un enllaç intern per fer la vinculació",
        null=True,
        blank=True
    )
    mostrar_titulo = models.BooleanField(
        default=True, 
        verbose_name="Mostrar títol"
    )
    mostrar_descripcion = models.BooleanField(
        default=True, 
        verbose_name="Mostrar descripció"
    )
    
    link_generico = models.URLField(
        blank=True,
        null=True,
        help_text="Enllaç oblogatori quan no tenim viculat un descatat viculat.",
        verbose_name="Enlla genèric"
    )

    flyer = models.ImageField(
        upload_to='personalizacion/flyers/',
        help_text="Puja el flyer de l'esdeveniment en format DIN A3",
        null=True,
        blank=True,
        verbose_name="Flyer"
    )
    color = ColorField(
        default='#FFFFFF',
        verbose_name="Color"
    )
    personalizacion = models.ForeignKey(
        Personalizacion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Personalització",
    )

    orden = models.PositiveIntegerField(
        default=0,
        help_text="Defineix l'ordre del destacat",
        verbose_name="Ordre"
    )
    
    def clean(self):
        # Valida que si `destacado` no está definido, `link_generico` debe ser obligatorio
        if not self.destacado and not self.link_generico:
            raise ValidationError("Si no se especifica un 'Destacat', el 'Enllaç genèric' es obligatorio.")
        

    def __str__(self):
        return f"Super Descat: {self.titulo}"

    class Meta:
        ordering = ['orden']
        verbose_name = "Super destacat"
        verbose_name_plural = "Super destacats"




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