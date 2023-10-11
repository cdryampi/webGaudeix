from django.db import models

from singleton_model import SingletonModel

from blog.models import Post, Categoria, SubBlog

from subvenciones.models import SubvencionDescripcion

from paginas_estaticas.models import Contacto, PuntoInformacion

from eventos_especiales.models import EventoEspecial

from compra_y_descubre.models import CompraDescubre

from django.core.exceptions import ValidationError

from colorfield.fields import ColorField

from django.conf import settings

import pdb

class Header(SingletonModel):
    logo = models.ImageField(
        upload_to='logo/'
    )
    color_fondo_header = ColorField(
        default='#0000'
    )
    color_letra = ColorField(
        default='#FFFFFF'
    )

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
            evento_especial = None,
            subvencion = None,
            compra_y_descubre = None,
            contacto= None
        ).delete()

        super().save(*args, **kwargs)
    
    def get_logo_absolute_url(self):
        return settings.DOMAIN_URL + self.logo.url

class HeaderFooter(SingletonModel):
    color_fondo_header = ColorField(
        default='#0000'
    )
    color_letra = ColorField(
        default='#FFFFFF'
    )

    def __str__(self):
        return "Menú del footer"
    
    def save(self, *args, **kwargs):
        # Eliminar referencias sin vínculos
        Referencia.objects.filter(
            header_footer=self,
            post=None,
            categoria=None,
            subblog=None,
            externo=None,
            evento_especial = None,
            contacto= None,
            subvencion = None,
            compra_y_descubre= None

        ).delete()

        super().save(*args, **kwargs)

class EnlaceExterno(models.Model):
    """
        Modelo que representa una enlace externo.
    """
    titulo = models.CharField(
        max_length=35,
        help_text="Títol de l'enllaç",
        verbose_name="títol"
    )
    enlace = models.URLField(
        blank=True,
        null=True,
        help_text="Enllaç extern",
        verbose_name="enllaç"
    )


    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name_plural = "Enllaços externs"
        verbose_name = "Enllaç extern"

class Referencia(models.Model):
    TIPOS_REFERENCIA = (
        ('post', 'entrada'),
        ('categoria', 'Categoría'),
        ('subblog', 'SubBlog'),
        ('externo', 'Enllaç Extern'),
        ('contacto','Contacte'),
        ('evento_especial','esdeveniment especial'),
        ('compra_y_descubre','Compra i Descobreix'),
        ('subvencion','Subvenció'),
        ('punt_informacio', "punt d'informació")
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPOS_REFERENCIA,
        help_text="selecciona el tipus de referencia que vols",
        verbose_name="Tipus"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Entrada"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name= "categoría"
    )
    subblog = models.ForeignKey(
        SubBlog,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    externo = models.ForeignKey(
        EnlaceExterno,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="extern"
    )
    contacto = models.ForeignKey(
        Contacto,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="contacte"
    )
    evento_especial = models.ForeignKey(
        EventoEspecial,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="esdeveniment"
    )
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name="ordre"
    )
    punt_informacio = models.ForeignKey(
        PuntoInformacion,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="punt d'informació"
    )
    header = models.ForeignKey(
        Header,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=1,
        verbose_name="capcelera"
    )
    header_footer = models.ForeignKey(
        HeaderFooter,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="capcelera inferior"
    )
    subvencion = models.ForeignKey(
        SubvencionDescripcion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="subvenció"
    )
    compra_y_descubre = models.ForeignKey(
        CompraDescubre,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="compra i descobreix"
    )
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
        elif self.subvencion:
            titulo = self.subvencion.titulo
        elif self.punt_informacio:
            titulo = self.punt_informacio.titulo
        elif self.compra_y_descubre:
            titulo = self.compra_y_descubre.titulo

        return f"{tipo}: {titulo}"


    def save(self, *args, **kwargs):

        if self.tipo == 'post':

            self.categoria = None
            self.subblog = None
            self.externo = None
            self.contacto = None  # Nueva línea: Limpiar el campo 'contacto'
            self.evento_especial = None
            self.subvencion = None
            self.punt_informacio = None
            self.compra_y_descubre = None

        elif self.tipo == 'categoria':

            self.post = None
            self.subblog = None
            self.externo = None
            self.contacto = None  # Nueva línea: Limpiar el campo 'contacto'
            self.evento_especial = None
            self.subvencion = None
            self.punt_informacio = None
            self.compra_y_descubre = None

        elif self.tipo == 'subblog':

            self.post = None
            self.categoria = None
            self.externo = None
            self.contacto = None  # Nueva línea: Limpiar el campo 'contacto'
            self.evento_especial = None
            self.subvencion = None
            self.punt_informacio = None
            self.compra_y_descubre = None

        elif self.tipo == 'externo':
            
            self.post = None
            self.categoria = None
            self.subblog = None
            self.contacto = None  # Nueva línea: Limpiar el campo 'contacto'
            self.evento_especial = None
            self.subvencion = None
            self.punt_informacio = None
            self.compra_y_descubre = None

        elif self.tipo == 'contacto':  # Nueva condición para el tipo 'contacto'

            self.post = None
            self.categoria = None
            self.subblog = None
            self.externo = None
            self.evento_especial = None
            self.subvencion = None
            self.punt_informacio = None
            self.compra_y_descubre = None

        elif self.tipo == 'evento_especial':

            self.post = None
            self.categoria = None
            self.subblog = None
            self.externo = None
            self.contacto = None
            self.subvencion = None
            self.punt_informacio = None
            self.compra_y_descubre = None

        elif self.tipo == 'subvencion':
            self.post = None
            self.categoria = None
            self.subblog = None
            self.externo = None
            self.contacto = None
            self.evento_especial = None
            self.punt_informacio = None
            self.compra_y_descubre = None

        elif self.punt_informacio == 'punt_informacio':

            self.post = None
            self.categoria = None
            self.subblog = None
            self.externo = None
            self.contacto = None
            self.evento_especial = None
            self.subvencion = None
            self.compra_y_descubre = None

        elif self.compra_y_descubre == 'compra_y_descubre':
            self.post = None
            self.categoria = None
            self.subblog = None
            self.externo = None
            self.contacto = None
            self.evento_especial = None
            self.subvencion = None
            self.punt_informacio = None


        if not self.post and not self.categoria and not self.subblog and not self.externo and not self.contacto and not self.evento_especial and not self.compra_y_descubre and not self.subvencion and not self.punt_informacio:
            return
            
        if self.header and self.header_footer:
            raise ValidationError("Només pots seleccionar un tipus d'encapçalament")

        super().save(*args, **kwargs)


    class Meta:
        ordering = ['orden']
