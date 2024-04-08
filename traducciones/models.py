from django.db import models
from django.conf import settings
import os

class Translation(models.Model):
    """
    Clase que representa a un lenguaje y su fichero de traducción.
    """
    LANGUAGE_CHOICES = [
        ('ca', 'Català'),
        ('es', 'Espanyol'),
        ('en', 'Anglès'),
        ('fr', 'Francès'),
    ]

    language_code = models.CharField(
        max_length=2,  # Actualizado para reflejar el tamaño estándar de los códigos de idioma ISO 639-1
        choices=LANGUAGE_CHOICES,
        unique=True,
        default= "ca"
    )

    def __str__(self):
        return self.get_language_code_display()  # Devuelve la representación en texto del idioma

    class Meta:
        verbose_name = "Traducció"
        verbose_name_plural = "Traduccions"

    @property
    def po_file_path(self):
        """Devuelve la ruta al archivo .po basada en el código de idioma."""
        return os.path.join(settings.BASE_DIR, 'locale', self.language_code, 'LC_MESSAGES', 'django.po')

    def get_po_file_content(self):
        """Lee y devuelve el contenido del archivo .po asociado."""
        try:
            with open(self.po_file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return "Archivo .po no encontrado."

    def save_po_file_content(self, content):
        """Guarda el contenido modificado en el archivo .po asociado."""
        with open(self.po_file_path, 'w', encoding='utf-8') as file:
            file.write(content)
