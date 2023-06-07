from django.db import models
from paginas_estaticas.models import PaginaLegal

# Create your models here.
class FooterManager(models.Manager):
    def get_singleton(self):
        # Verificar si ya existe una instancia de Footer
        if self.exists():
            # Si existe, retornar la primera instancia encontrada
            return self.first()

        # Si no existe, crear una nueva instancia de Footer y guardarla
        footer = self.create()
        return footer
    
class Footer(models.Model):
    # Atributos del footer
    title = models.CharField(max_length=100)
    description = models.TextField()

    objects = FooterManager()

    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footer"

    def __str__(self):
        return self.title

class FooterEmpresa(models.Model):
    # Atributos del footer de empresas
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='footer_empresas/',help_text='Agrega una imagen(143 x 72 px) relevante para el diseño del footer.')
    enlace = models.URLField(null=True, blank=True)
    footer = models.ForeignKey(Footer, on_delete=models.CASCADE, related_name='empresas',default=1)

    class Meta:
        verbose_name = "Footer Empresa"
        verbose_name_plural = "Footer Empresas"

    def __str__(self):
        return f'Footer Empresa: {self.id}'

class FooterInformacion(models.Model):
    imagen = models.ImageField(upload_to='footer/', help_text='Agrega una imagen relevante para la información del footer.')
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo_contacto = models.EmailField()
    paginas_legales = models.ManyToManyField(PaginaLegal)
    footer = models.OneToOneField(Footer, on_delete=models.CASCADE,default=1)
    def __str__(self):
        return 'Información del Footer'