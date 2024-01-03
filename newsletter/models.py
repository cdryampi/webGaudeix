from django.db import models
from eventos_especiales.models import EventoEspecial
from django.core.files.base import ContentFile
from .utils import gen_html_evento_especial
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
        # Genera el contenido HTML utilizando tu plantilla y los datos del evento
        html_content = gen_html_evento_especial(self, self.evento_especial)
        # Guarda el contenido HTML en un archivo
        self.html_file.save(f'newsletter-{self.id}.html', ContentFile(html_content))

    class Meta:
        verbose_name_plural = "Newsletters"