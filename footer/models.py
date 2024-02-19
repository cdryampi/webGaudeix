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
    titulo = models.CharField(
        max_length=100,
        verbose_name="Títol",
        help_text="Afegeix un títol per a l'empresa en el footer."
    )

    imagen = models.ImageField(
        upload_to='footer_empresas/',
        verbose_name="Imatge",
        help_text='Afegeix una imatge (143 x 72 px) rellevant per al disseny del footer.'
    )

    enlace = models.URLField(
        null=True,
        blank=True,
        verbose_name="Enllaç",
        help_text="Afegeix un enllaç opcional per a l'empresa."
    )

    footer = models.ForeignKey(
        Footer,
        on_delete=models.CASCADE,
        verbose_name="Footer associat",
        help_text="Selecciona el footer al qual pertany l'empresa."
    )

    class Meta:
        verbose_name = "Footer Empresa"
        verbose_name_plural = "Footer Empresas"

    def __str__(self):
        return f'Footer Empresa: {self.id}'

class FooterInformacion(models.Model):
    imagen = models.ImageField(
        upload_to='footer/',
        verbose_name="Imatge",
        help_text='Afegeix una imatge rellevant per a la informació del footer.'
    )
    direccion = models.CharField(
        max_length=100,
        verbose_name="Direcció",
        help_text="Especifica la direcció de contacte."
    )
    telefono = models.CharField(
        max_length=20,
        verbose_name="Telèfon",
        help_text="Afegeix el número de telèfon de contacte."
    )
    correo_contacto = models.EmailField(
        verbose_name="Correu de contacte",
        help_text="Afegeix l'adreça de correu electrònic de contacte."
    )
    paginas_legales = models.ManyToManyField(
        PaginaLegal,
        verbose_name="Pàgines legals",
        help_text="Selecciona les pàgines legals vinculades a la informació del footer."
    )
    footer = models.OneToOneField(Footer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Informació del Footer"
        verbose_name_plural = "Informacions del Footer"

    def __str__(self):
        return 'Informació del Footer'