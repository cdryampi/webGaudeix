from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class TeenvioManager(models.Manager):

    def get_singleton(self):
        # Verificar si ya existe una instancia de Teenvio
        if self.exists():
            # Si existe, retornar la primera instancia encontrada
            return self.first()
        
        # Si no existe, crear una nueva instancia de Teenvio y guardarla
        teenvio = self.create()
        return teenvio
    def create(self, **kwargs):
        # Verificar si ya existe una instancia de Teenvio
        if self.exists():
            raise ValueError("Ya existe una instancia de Teenvio")

        return super().create(**kwargs)


class Teenvio(models.Model):
    ACTION_CHOICES = (
        ('contact_save', 'Guardar contacto'),
        # Agrega aquí otros choices según tus necesidades
    )

    gid = models.CharField(
        max_length=100,
        help_text="Identificador de Teenvio"
    )
    user = models.CharField(
        max_length=100,
        help_text="Nombre de usuario de Teenvio",
        verbose_name="Nom d'usuari de Teenvio"
    )
    password = models.CharField(
        max_length=100,
        help_text="Contraseña de Teenvio",
        verbose_name="contrasenya"
    )
    plan = models.CharField(
        max_length=100,
        help_text="Plan de Teenvio",
        verbose_name="Pla"
    )
    url = models.URLField(
        default="https://master5.teenvio.com/v4/public/api/v3/post/",
        help_text="URL de la API de Teenvio",
        verbose_name="URL"
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        default='contact_save',
        help_text="Acció per defecte",
        verbose_name="Acció"
    )

    objects = TeenvioManager()

    class Meta:
        verbose_name = "API Teenvio"
        verbose_name_plural = "API Teenvio"

    def __str__(self):
        return "API Teenvio"

    def save(self, *args, **kwargs):
        if Teenvio.objects.exists():
            raise ValidationError("Ya existe una instancia de Teenvio.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Evitar borrar la instancia de Teenvio
        pass



class Subscriptor(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Nom",
        help_text="Nom del subscriptor"
    )
    email = models.EmailField(
        verbose_name="Correu electrònic",
        help_text="Correu electrònic del subscriptor"
    )
    exportable = models.BooleanField(
        default=True,
        verbose_name="exportable",
        help_text="El subscriptor és exportable?"
    )
    sincronizado = models.BooleanField(
        default=False,
        verbose_name="sincronitzat",
        help_text="El subscriptor està sincronitzat?"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Donat d'alta",
        help_text="Dada de donació."
    )
    def __str__(self):
        return self.name
