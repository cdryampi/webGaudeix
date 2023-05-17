from django.db import models

# Create your models here.
class PersonalizacionManager(models.Manager):
    def get_singleton(self):
        # Verificar si ya existe una instancia de Personalizacion
        if self.exists():
            # Si existe, retornar la primera instancia encontrada
            return self.first()

        # Si no existe, crear una nueva instancia de Personalizacion y guardarla
        personalizacion = self.create()
        return personalizacion

class Favicon(models.Model):
    image = models.ImageField(upload_to='favicons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favicon"
        verbose_name_plural = "Favicons"

    def __str__(self):
        return f"Favicon {self.id}"

    @property
    def description(self):
        return "Este favicon se utiliza como icono de la pestaña del navegador para identificar tu sitio web."


class Personalizacion(models.Model):
    # Atributos del modelo
    favicon = models.OneToOneField(Favicon, on_delete=models.SET_NULL, null=True, blank=True)

    objects = PersonalizacionManager()

    class Meta:
        verbose_name = "Personalización"
        verbose_name_plural = "Personalización"

    def save(self, *args, **kwargs):
        # Solo se permite guardar una única instancia de Personalizacion
        if Personalizacion.objects.exists() and not self.pk:
            raise ValueError("Ya existe una instancia de Personalizacion. No se puede crear otra.")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # No se permite eliminar la instancia de Personalizacion
        raise ValueError("No se puede eliminar la instancia de Personalizacion.")

