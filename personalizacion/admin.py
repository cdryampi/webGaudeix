from django.contrib import admin
from .models import InternalLink, Personalizacion, TrenPersonalizacion, BusPersonalizacion, AeropuertoPersonalizacion, AutoPistaPersonalizacion, AgendaParallax, InternalLink, SuperDestacado
from django.http import HttpResponseRedirect
from django.core.files.storage import default_storage
from gaudeix import settings
import os



def eliminar_archivos_ics(modeladmin, request, queryset):
    directorio_ics = os.path.join(settings.BASE_DIR, 'media')  # Ajustar según la ubicación exacta
    for archivo in os.listdir(directorio_ics):
        if archivo.endswith('.ics'):
            os.remove(os.path.join(directorio_ics, archivo))
    modeladmin.message_user(request, "Fitxers '.ics' temporals eliminats.")
eliminar_archivos_ics.short_description = "Eliminar fitxers ICS."


class TrenPersonalizacionAdminInLine(admin.StackedInline):
    model = TrenPersonalizacion
    extra = 1

class BusPersonalizacionAdminInLine(admin.StackedInline):
    model = BusPersonalizacion
    extra = 1

class AeropuertoPErsonalizacionAdminInLine(admin.StackedInline):
    model = AeropuertoPersonalizacion
    extra = 1

class AutoPistaPersonalizacionAdminInLine(admin.StackedInline):
    model = AutoPistaPersonalizacion
    extra = 1










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


class SuperDestacadoAdmin(admin.ModelAdmin):
    model = SuperDestacado
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'descripcion',
                'destacado',
            ],
            'description': (
                "<p>Super destacta per l'inici.</p>"
                "<p>Aquest model fa que puguis afegir una referència del model 'enllaç intern' cap personalització.</p>"
                "<p>Pots afegir una descripció per l'encapçalament la secció del super destacat, si no poses res afegirà un 'No et pots perdre'.</p>"
                "<p>S'ha de tenir en compte que s'ha pensat per poder destacar encara més els esdeveniments especials i els esdeveniments compra i descobreix.</p>"
                "<p>El sistema agafarà en el cas dels esdeveniments especials la imatge del parallax que té assignat o la primera imatge de la seva galeria, en cas que no hi hagi imatges agafarà una per defecte.</p>"
                "<p>El sistema agafarà en el cas dels esdeveniments de 'compra i descobreix' de la imatge principal en cas que no hi hagin vinculat les imatges, agafarà una imatge per defecte.</p>"
            ),
        }),
    ]  


class PersonalizacionAdmin(admin.ModelAdmin):

    search_fields = ['topbar','meta_keywords']

    fieldsets = [
        (None, {
            'fields': [
                'favicon',
                'parallax_portada',
                'parallax_agenda',
                'super_destacado',
                'video_portada',
                'topbar',
                'horario',
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
                "<p><strong>Nota:</strong> Si utilitzes Google Analytics, assegura't de mantenir actualitzat el script de Google Analytics en el camp 'Script de Google Analytics' quan sigui necessari per a un seguiment precís.</p>"
                "<p>Nota: a 2023 encara tenim el canvi d'horari, llavors per l'hivern fes servir l'horari de l'hivern que resta 1 hora de més els enllaços del Google Calendar que fem servir als esdeveniments.</p>"
            ),

        }),
    ]

    inlines = [TrenPersonalizacionAdminInLine, BusPersonalizacionAdminInLine, AeropuertoPErsonalizacionAdminInLine, AutoPistaPersonalizacionAdminInLine]
    actions = [eliminar_archivos_ics]


admin.site.register(Personalizacion, PersonalizacionAdmin)
admin.site.register(AgendaParallax, AgendaParallaxAdmin)
admin.site.register(SuperDestacado, SuperDestacadoAdmin)
admin.site.register(InternalLink, InternalLinkAdmin)