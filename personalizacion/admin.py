from django.contrib import admin
from .models import InternalLink, Personalizacion, TrenPersonalizacion, BusPersonalizacion, AeropuertoPersonalizacion, AutoPistaPersonalizacion, AgendaParallax, InternalLink, SuperDestacado, IframeVideoHome
from django.http import HttpResponseRedirect
from django.core.files.storage import default_storage
from gaudeix import settings
from newsletter.models import Newsletter
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from multimedia_manager.models import Carrusel, ImagenCarrusel
import os
from django.conf import settings



def eliminar_archivos_ics(modeladmin, request, queryset):
    directorio_ics = os.path.join(settings.BASE_DIR, 'media')  # Ajustar según la ubicación exacta
    for archivo in os.listdir(directorio_ics):
        if archivo.endswith('.ics'):
            os.remove(os.path.join(directorio_ics, archivo))
    modeladmin.message_user(request, "Fitxers '.ics' temporals eliminats.")
eliminar_archivos_ics.short_description = "Eliminar fitxers ICS."


def eliminar_archivos_html_newsletter(modeladmin, request, queryset):
    directorio_newsletter = os.path.join(settings.MEDIA_ROOT, 'newsletters')
    archivos_eliminados = 0

    # Eliminar físicamente los archivos HTML
    for archivo in os.listdir(directorio_newsletter):
        if archivo.endswith('.html'):
            os.remove(os.path.join(directorio_newsletter, archivo))
            archivos_eliminados += 1

    # Limpiar las referencias en el modelo para todos los campos traducidos
    for newsletter in Newsletter.objects.all():
        campos_html_limpiados = False
        for codigo_idioma, _ in settings.LANGUAGES:
            field_name = f'html_file_{codigo_idioma}'
            file_field = getattr(newsletter, field_name, None)
            if file_field and file_field.name:
                path_archivo = os.path.join(directorio_newsletter, file_field.name)
                if not os.path.isfile(path_archivo):
                    setattr(newsletter, field_name, None)
                    campos_html_limpiados = True
        if campos_html_limpiados:
            newsletter.save()

    modeladmin.message_user(request, f"Fitxers '.html' de les plantilles eliminats. Total: {archivos_eliminados}")
eliminar_archivos_html_newsletter.short_description = "Eliminar fitxers HTML."





class TrenPersonalizacionAdminInLine(TranslationStackedInline):
    model = TrenPersonalizacion
    extra = 1

class BusPersonalizacionAdminInLine(TranslationStackedInline):
    model = BusPersonalizacion
    extra = 1

class AeropuertoPErsonalizacionAdminInLine(TranslationStackedInline):
    model = AeropuertoPersonalizacion
    extra = 1

class AutoPistaPersonalizacionAdminInLine(TranslationStackedInline):
    model = AutoPistaPersonalizacion
    extra = 1




class ImagenCarruselInline(TranslationStackedInline):  # O usa admin.StackedInline para un estilo diferente
    model = ImagenCarrusel
    extra = 1  # Número de formularios para imágenes nuevas
    fields = ['imagen', 'descripcion', 'orden']
    verbose_name = "Imatge del carrusel"
    verbose_name_plural = "Imatges del carrusel"

class CarruselAdmin(admin.ModelAdmin):
    inlines = [ImagenCarruselInline]
    fieldsets = [
        (None, {
            'fields': ['titulo', 'descripcion', 'tipo', 'activo'],
            'description': (
                "<p>Defineix un carrusel d'imatges per ser mostrat en diferents parts del lloc web.</p>"
                "<p>Aquest model permet afegir diverses imatges i ordenar-les segons la necessitat.</p>"
                "<p>Pots utilitzar aquestes imatges per destacar contingut, promocions, esdeveniments o qualsevol cosa que consideris important.</p>"
                "<p>Recorda que l'ordre de les imatges es pot ajustar dins de la secció de 'Imatges del carrusel'.</p>"
            ),
        }),
    ]
    list_display = ('titulo', 'activo')
    list_filter = ('activo',)
    search_fields = ['titulo', 'descripcion']



class InternalLinkAdmin(admin.ModelAdmin):
    model = InternalLink
    autocomplete_fields = ('evento_especial', 'compra_y_descubre')
    fieldsets = [
        (None, {
            'fields': [
                'tipo',
                'evento_especial',
                'compra_y_descubre',
            ],
            'description': (
                "<p>Enllaç intern per afegir referències cap als models d''esdeveniments especials' i 'compra i descobreix'.</p>"
                "<p>En aquest model pots afegir tantes referències com vulguis.</p>"
                "<p>S'ha de tenir en compte que només es pot afegir els esdeveniments compra i descobreix.</p>"
            ),
        }),
    ]


class AgendaParallaxAdmin(admin.ModelAdmin):
    model = AgendaParallax
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'parallax_agenda'
            ],
            'description': (
                "<p>Parallax per l'agenda.</p>"
                "<p>Aquest model fa que puguis fer servir els mateixos parallax dels altres models a personalització.</p>"
                "<p>S'ha de tenir en compte fer servir títols descriptius amb coherència per poder identificar els parallax per l'agenda.</p>"
            ),
        }),
    ]


class IframVideoHomeAdmin(TranslationAdmin ,admin.ModelAdmin):
    model = IframeVideoHome
    fieldsets = [
        (None, {
            'fields': [
                'internal_name',
                'title',
                'description',
                'video_url',
            ],
            'description': (
                "<p>Configura el vídeo auxiliar per a la portada del teu lloc web.</p>"
                "<p>Aquest model permet utilitzar vídeos específics com a part del disseny visual de la portada, "
                "millorant la interacció i l'experiència visual de l'usuari.</p>"
                "<p>Assegura't de seleccionar vídeos que compleixin amb les necessitats de privacitat i que estiguin habilitats per a la incrustació.</p>"
                "<p>Utilitza noms interns descriptius per facilitar la gestió i identificació dels vídeos en el sistema.</p>"
            ),
        }),
    ]



class SuperDestacadoAdmin(TranslationStackedInline):
    model = SuperDestacado
    extra = 1
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'descripcion',
                'destacado',
                'mostrar_titulo',
                'mostrar_descripcion',
                'orden',
                'personalizacion'
            ],
            'description': (
                "<p>Super destacat per a l'inici.</p>"
                "<p>Aquest model permet afegir una referència al model 'esdeveniment especial'.</p>"
                "<p>Pots afegir una descripció per a l'encapçalament de la secció del super destacat.</p>"
                "<p>Es considera especialment útil per a destacar encara més els esdeveniments especials i els esdeveniments de 'compra i descobreix - comerç local'.</p>"
                "<p>En el cas d'esdeveniments especials, el sistema utilitzarà la imatge del parallax assignat o la primera imatge de la seva galeria. Si no hi ha imatges disponibles, es mostrarà una imatge per defecte.</p>"
                "<p>Per als esdeveniments de 'compra i descobreix', el sistema utilitzarà la imatge principal. En absència d'imatges vinculades, es recorrerà a una imatge per defecte.</p>"
                "<p><strong>Nota:</strong> Si s'incorpora un flyer (programa en format DIN A3), el sistema seleccionarà entre dues plantilles diferents basant-se en la presència d'aquest i el donarà prioritat.</p>"
            ),
        }),
    ]  


class PersonalizacionAdmin(TranslationAdmin, admin.ModelAdmin):

    search_fields = ['topbar','meta_keywords']

    fieldsets = [
        (None, {
            'fields': [
                'favicon',
                'carrusel_portada',
                'carrusel_agenda',
                'parallax_portada',
                'parallax_agenda',
                'video_portada',
                'topbar',
                'horario',
                'dias_vista_agenda',
                'enlace_agenda',
                'video_url',
                'hora_agenda_fin',
                'analytics_script',
                'meta_keywords',
                'meta_description_portada'
            ],
            'description': (
                "<p>Configura la personalització del teu lloc web.</p>"
                "<p>Aquí pots ajustar aspectes visuals i funcionals per adaptar el teu lloc a les teves necessitats.</p>"
                "<p>Personalitza el favicon, afegeix efectes de parallax i selecciona un vídeo per a la portada.</p>"
                "<p>Aquí pots seleccionar el parallax per l'agenda que més t'agradi.</p>"
                "<p>Crea una barra superior amb informació destacada i enllaços importants per als teus usuaris.</p>"
                "<p>Recorda tenir només una barra superior activa a la vegada per evitar resultats no desitjats.</p>"
                "<p>Afegeix aquí l'URL de l'iframe del vídeo que desitgis utilitzar com a vídeo a una part de la portada.</p>"
                "<p><strong>Nota:</strong> Si utilitzes Google Analytics, assegura't de mantenir actualitzat el script de Google Analytics en el camp 'Script de Google Analytics' quan sigui necessari per a un seguiment precís.</p>"
                "<p><strong>Nota:</strong> a 2023 encara tenim el canvi d'horari, llavors per l'hivern fes servir l'horari de l'hivern que resta 1 hora de més els enllaços del Google Calendar que fem servir als esdeveniments.</p>"
                
            ),

        }),
    ]

    inlines = [TrenPersonalizacionAdminInLine, BusPersonalizacionAdminInLine, AeropuertoPErsonalizacionAdminInLine, AutoPistaPersonalizacionAdminInLine, SuperDestacadoAdmin]
    actions = [eliminar_archivos_ics,eliminar_archivos_html_newsletter]

admin.site.register(Carrusel, CarruselAdmin)
admin.site.register(Personalizacion, PersonalizacionAdmin)
admin.site.register(AgendaParallax, AgendaParallaxAdmin)
admin.site.register(InternalLink, InternalLinkAdmin)
admin.site.register(IframeVideoHome, IframVideoHomeAdmin)