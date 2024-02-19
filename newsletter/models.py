from django.db import models
from django.utils import translation
from eventos_especiales.models import EventoEspecial
from django.core.files.base import ContentFile
from .utils import gen_html_evento_especial
from django.conf import settings
# Create your models here.

class Newsletter(models.Model):
    evento_especial = models.ForeignKey(
        EventoEspecial,
        on_delete= models.CASCADE,
        help_text="Afegeix l'esdeveniment que vols",
        verbose_name="Esdeveniment especial"
    )
    nombre_interno = models.CharField(
        max_length=200,
        help_text="Afegeix un nom especial per poder descriure millor la teva Newsletter",
        verbose_name="nom intern"
    )
    html_file = models.FileField(
        upload_to='newsletters/',
        null=True,
        blank=True,
        editable=False,
        help_text="Aquest fitxer es genera des del llistat de newsletter.",
        verbose_name="Plantilla HTML."
    )

    link_tracking = models.URLField(
        null=True,
        blank=True,
        verbose_name = "enllaç per fer tracking.",
        help_text =  "afegeix l'ellaç per fer tracking. També l'enllaç té que portar una redirecció cap a la web de Gaudeix."
    )

    subtitulo = models.TextField(
        null=True,
        blank=True,
        verbose_name="subtìtul",
        help_text="afegeix un subtìtul o el nom de l'esdeveniment PE: 'Festa del Nadal'."
    )

    def __str__(self):
        return f"Newsletter per a {self.nombre_interno} - {self.evento_especial.titulo}"

    def generar_y_guardar_html(self):
        idioma_actual = translation.get_language()  # Guardar el idioma actual
        for codigo_idioma, _ in settings.LANGUAGES:
            translation.activate(codigo_idioma)  # Activar el idioma para la generación de contenido

            # Genera el contenido HTML utilizando tu plantilla y los datos del evento
            html_content = gen_html_evento_especial(self, self.evento_especial)
            
            # Construir el nombre del archivo incluyendo el código de idioma
            nombre_archivo = f'newsletter-{self.id}-{codigo_idioma}.html'
            
            # Construir el nombre del campo basado en el idioma
            field_name = f'html_file_{codigo_idioma}'
            
            # Guardar el contenido HTML en el campo de archivo traducido correspondiente
            file_field = getattr(self, field_name, None)
            if file_field is not None:
                file_field.save(nombre_archivo, ContentFile(html_content), save=False)
        
        self.save()  # Asegúrate de guardar el modelo después de actualizar los archivos
        translation.activate(idioma_actual)  # Restaurar el idioma original

    class Meta:
        verbose_name_plural = "Newsletters"