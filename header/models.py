from django.db import models
from singleton_model import SingletonModel
from blog.models import Post, Categoria, SubBlog
from django.core.exceptions import ValidationError

class Header(SingletonModel):
    logo = models.ImageField(upload_to='logo/')

    def __str__(self):
        return "Menú de navegación"


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
    enlace = models.URLField(blank=True, null=True)
    header = models.ForeignKey(Header, on_delete=models.CASCADE, null=True, blank=True, default=1)

    def __str__(self):
        return self.tipo

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

