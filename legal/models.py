from typing import Iterable, Optional
from django.db import models

# Create your models here.
from django.db import models
from ckeditor.fields import RichTextField

class PaginaLegal(models.Model):
    TIPOS = (
        ('privacitat', 'Política de privacitat'),
        ('avis_legal', 'Avís legal'),
        ('cookies', 'Política de cookies'),
    )

    tipo = models.CharField(max_length=20, choices=TIPOS, unique=True) # Campo para almacenar el tipo de página legal
    encabezado = models.CharField(max_length=200) # Campo para el encabezado de la página
    imagen = models.ImageField(upload_to='legal_images/') # Campo para la imagen asociada a la página
    contenido = RichTextField() # Campo para el contenido de la página

    def __str__(self):
        return self.get_tipo_display()
    def save(self, *args, **kwargs):
        # Verificar si ya existe una instancia con el mismo tipo
        if not self.pk and PaginaLegal.objects.filter(tipo=self.tipo).exists():
            raise ValueError(f"Ya existe una instancia de {self.tipo}.")
        return super().save(*args, **kwargs)
