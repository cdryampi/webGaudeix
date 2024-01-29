from django.db import models
from multimedia_manager.models import Imagen, Fichero
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from colorfield.fields import ColorField


class Alerta(models.Model):
    """
        Modelo que representa a una alerta
    """

    titulo = models.CharField(
        max_length=200, 
        verbose_name="títol", 
        help_text="Introdueix el títol de l'alerta"
    )
    descripcion = models.TextField(
        max_length = 255,
        validators=[MaxLengthValidator(255)],
        verbose_name="descripció", 
        help_text="Escriu una descripció detallada de l'alerta"
    )
    fecha_inicio = models.DateTimeField(
        verbose_name="data d'inici", 
        help_text="Selecciona quan comença l'alerta"
    )
    fecha_fin = models.DateTimeField(
        verbose_name="data de finalització", 
        help_text="Selecciona quan finalitza l'alerta"
    )
    imagen = models.ForeignKey(
        Imagen,
        on_delete= models.CASCADE,
        verbose_name="imatge", 
        help_text="Puja una imatge relacionada amb l'alerta (opcional)"
    )
    ver_mas = models.URLField(
        blank=True,
        help_text="Afegeix un enllaç per donar més informació de l'alerta. (opcional)",
        verbose_name= "Enllaç",
        null=True
    )

    fichero = models.OneToOneField(
        Fichero,
        on_delete=models.CASCADE,
        verbose_name="Fitxer",
        help_text="Afegeix un fitxer pdf.",
        blank=True,
        null=True
    )
    color = ColorField(
        default='#000000',
        verbose_name="Color",
        help_text="Selecciona un color pel disseny de l'alerta."
    )

    publicado = models.BooleanField(
        default=False,
        verbose_name="Publicat",
        help_text="Marca si l'alerta està activa"
    )

    def __str__(self):
        return self.titulo
    
    def delete(self, *args, **kwargs):
        self.imagen.delete()
        self.fichero.delete()
        super().delete(*args, **kwargs)

    def has_init(self):
        """
            Función que retorna un valor boleano cuando la fecha actual no ha superado la fecha de inicio y es menor a la fecha del fin.
        """
        now = timezone.now()

        return self.fecha_inicio <= now and self.fecha_fin >= now

    def clean(self):
        # Verifica que la fecha de inicio no sea posterior a la fecha de fin
        if self.fecha_inicio and self.fecha_fin and self.fecha_inicio > self.fecha_fin:
            raise ValidationError(_('La fecha de inicio debe ser anterior a la fecha de fin.'))
    
    def save(self, *args, **kwargs):
        self.clean()
        super(Alerta, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "alerta"
        verbose_name_plural = "alertes"
