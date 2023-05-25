from django.db import models
from singleton_model import SingletonModel
from blog.models import Post, Categoria, SubBlog
from django.core.exceptions import ValidationError




class Header(SingletonModel):
    logo = models.ImageField(upload_to='logo/')

    def __str__(self):
        return "Menú de navegación"

class EnlaceExterno(models.Model):
    titulo = models.CharField(max_length=15, help_text="Títol de l'enllaç")
    enlace = models.URLField(blank=True, null=True, help_text="Enllaç extern")


    def __str__(self):
        return self.titulo

class Referencia(models.Model):
    TIPOS_REFERENCIA = (
        ('post', 'Post'),
        ('categoria', 'Categoría'),
        ('subblog', 'SubBlog'),
        ('externo', 'Enlace Externo'),
    )

    tipo = models.CharField(max_length=10, choices=TIPOS_REFERENCIA)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
    subblog = models.ForeignKey(SubBlog, on_delete=models.CASCADE, blank=True, null=True)
    externo = models.ForeignKey(EnlaceExterno, on_delete=models.CASCADE, blank=True, null=True)
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
            pass

        return f"{tipo}: {titulo}"


    def save(self, *args, **kwargs):
        if self.tipo == 'post':
            self.categoria = None
            self.subblog = None
            self.enlace = None
        elif self.tipo == 'categoria':
            self.post = None
            self.subblog = None
            self.enlace = None
        elif self.tipo == 'subblog':
            self.post = None
            self.categoria = None
            self.enlace = None
        elif self.tipo == 'externo':
            self.post = None
            self.categoria = None
            self.subblog = None

        super().save(*args, **kwargs)

