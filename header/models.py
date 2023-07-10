from django.db import models

from singleton_model import SingletonModel

from blog.models import Post, Categoria, SubBlog

from paginas_estaticas.models import Contacto

from eventos_especiales.models import EventoEspecial

from django.core.exceptions import ValidationError

from colorfield.fields import ColorField

class Header(SingletonModel):
    logo = models.ImageField(upload_to='logo/')
    color_fondo_header = ColorField(default='#0000')
    color_letra = ColorField(default='#FFFFFF')
    def __str__(self):
        return "Menú de navegación"
    def save(self, *args, **kwargs):
        # Eliminar referencias sin vínculos
        Referencia.objects.filter(
            header=self,
            post=None,
            categoria=None,
            subblog=None,
            externo=None,
            evento_especial = None
        ).delete()

        super().save(*args, **kwargs)



class EnlaceExterno(models.Model):
    titulo = models.CharField(max_length=35, help_text="Títol de l'enllaç")
    enlace = models.URLField(blank=True, null=True, help_text="Enllaç extern")


    def __str__(self):
        return self.titulo

class Referencia(models.Model):
    TIPOS_REFERENCIA = (
        ('post', 'Post'),
        ('categoria', 'Categoría'),
        ('subblog', 'SubBlog'),
        ('externo', 'Enlace Externo'),
        ('contacto','Contacto'),
        ('evento_especial','evento_especial')
    )

    tipo = models.CharField(max_length=30, choices=TIPOS_REFERENCIA)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
    subblog = models.ForeignKey(SubBlog, on_delete=models.CASCADE, blank=True, null=True)
    externo = models.ForeignKey(EnlaceExterno, on_delete=models.CASCADE, blank=True, null=True)
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, blank=True, null=True)
    evento_especial = models.ForeignKey(EventoEspecial, on_delete=models.CASCADE, blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)
    header = models.ForeignKey(Header, on_delete=models.CASCADE, null=True, blank=True, default=1)
    
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
        elif self.externo:
            titulo = self.externo.titulo
        elif self.contacto:
            titulo = self.contacto.titulo
        elif self.evento_especial:
            titulo = self.evento_especial.titulo

        return f"{tipo}: {titulo}"


    def save(self, *args, **kwargs):

        if self.tipo == 'post':

            self.categoria = None
            self.subblog = None
            self.externo = None
            self.contacto = None  # Nueva línea: Limpiar el campo 'contacto'
            self.evento_especial = None

        elif self.tipo == 'categoria':

            self.post = None
            self.subblog = None
            self.externo = None
            self.contacto = None  # Nueva línea: Limpiar el campo 'contacto'
            self.evento_especial = None

        elif self.tipo == 'subblog':

            self.post = None
            self.categoria = None
            self.externo = None
            self.contacto = None  # Nueva línea: Limpiar el campo 'contacto'
            self.evento_especial = None

        elif self.tipo == 'externo':
            self.post = None
            self.categoria = None
            self.subblog = None
            self.contacto = None  # Nueva línea: Limpiar el campo 'contacto'
            self.evento_especial = None

        elif self.tipo == 'contacto':  # Nueva condición para el tipo 'contacto'

            self.post = None
            self.categoria = None
            self.subblog = None
            self.externo = None
            self.evento_especial = None

        elif self.tipo == 'evento_especial':

            self.post = None
            self.categoria = None
            self.subblog = None
            self.externo = None
            self.contacto = None

        if not self.post and not self.categoria and not self.subblog and not self.externo and not self.contacto and not self.evento_especial:
            return
        
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['orden']
