from django.contrib import admin
from .models import Carrusel, Slide, InternalLink, Parallax, VideosEmbed, Personalizacion, TrenPersonalizacion, BusPersonalizacion, AeropuertoPersonalizacion, AutoPistaPersonalizacion, AgendaParallax
from blog.models import Tag
from django.contrib.admin.widgets import FilteredSelectMultiple
from .forms import CarruselForm
from django.core.exceptions import ValidationError
from multimedia_manager.models import Video
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms






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

class InternalLinkInline(admin.StackedInline):
    model = InternalLink
    extra = 1







class SlideAdmin(admin.ModelAdmin):
    inlines = [InternalLinkInline]

class CarruselAdmin(admin.ModelAdmin):
    form = CarruselForm






class PersonalizacionAdmin(admin.ModelAdmin):

    search_fields = ['topbar','meta_keywords']

    fieldsets = [
        (None, {
            'fields': [
                'favicon',
                'parallax_portada',
                'parallax_agenda',
                'video_portada',
                'topbar',
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
            ),

        }),
    ]
    
    inlines = [TrenPersonalizacionAdminInLine, BusPersonalizacionAdminInLine, AeropuertoPErsonalizacionAdminInLine, AutoPistaPersonalizacionAdminInLine]

admin.site.register(Personalizacion, PersonalizacionAdmin)
admin.site.register(Carrusel, CarruselAdmin)
admin.site.register(Slide,SlideAdmin)
admin.site.register(Parallax)
admin.site.register(AgendaParallax)
admin.site.register(VideosEmbed)
