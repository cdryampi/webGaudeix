from django.contrib import admin

# Register your models here.

from multimedia_manager.models import Fichero
from .models import EventoFichero, EventoEspecial, EventoEspecialGaleriaImagen
from django.db.models import Q
from multimedia_manager.models import Imagen
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from blog.models import Tag, Categoria
from django.http import HttpResponse


from django.http import FileResponse
import os


from django.utils.safestring import mark_safe


class EventoFicheroInline(admin.TabularInline):
    model = EventoFichero
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'fichero':
            evento_id = None
            if 'object_id' in request.resolver_match.kwargs:
                evento_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Fichero.objects.filter(
                Q(eventofichero__isnull=True) | Q(eventofichero__evento_id=evento_id),
                Q(postfichero__isnull=True),
                Q(pdfcollectionresoluciofichero__isnull =True),
                Q(pdfcollectionjustificaciofichero__isnull=True),
                Q(pdfcollectionconvocatoriafichero__isnull=True),
                Q(pdfcollectiontotesfichero__isnull = True),
                Q(pdfdiversidadfichero__isnull=True),
                Q(compradescubrefichero__isnull=True),
            )
            kwargs['empty_label'] = 'Sin fichero asociado'

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class EventoEspecialGaleriaImagenInline(admin.TabularInline):
    model = EventoEspecialGaleriaImagen
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            evento_especial = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                evento_especial = request.resolver_match.kwargs['object_id']
                #print(categoria_id)
                kwargs['queryset'] = Imagen.objects.filter(
                    Q(categoriabannerimagen__isnull=True),
                    Q(subblogimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True),
                    Q(postimagen__isnull=True),
                    Q(postgaleriaimagen__isnull=True),
                    Q(subbloggaleriaimagen__isnull=True),
                    Q(diversidadimagenbanner__isnull=True),
                    Q(compradescubrepasosimagen__isnull=True),
                    Q(compradescubreimagen__isnull=True),
                    Q(compradescubregaleriaimagen__isnull=True),
                    Q(eventoespecialgaleriaimagen__isnull=True) | Q(eventoespecialgaleriaimagen__evento_especial_id=evento_especial)
                )
            kwargs['empty_label'] = 'Sense imatge associada'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)





@admin.register(EventoEspecial)
class EventoEspecialAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_evento', 'publicado']
    list_filter = ['fecha_evento', 'publicado']
    search_fields = ['titulo']
    filter_horizontal = ('agendas', 'videos','tags')

    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'metatitulo',
                'descripcion_corta',
                'descripcion_larga',
                'metadescripcion',
                'fecha_evento',
                'fecha_fin',
                'publicado',
                'categoria',
                'color',
                'parallax',
                'display_qr_code',
                'download_qr_code',
                'agendas',
                'logo_especial',
                'imagen_especial',
                'tags',
                'videos',
            ],
            'description': (
                "<p><strong>Aquesta és la pàgina d'edició d'un esdeveniment especial.</strong></p>"
                "<p><em>Els <u>esdeveniments especials</u> són una part auxiliar del lloc web i pots crear-ne tants com desitgis.</em></p>"
                "<p>Assegura't de completar tots els camps i de marcar l'opció <strong>publicat</strong> perquè l'esdeveniment aparegui destacat a la web. També pots afegir un <strong>logo especial</strong> per destacar l'esdeveniment encara més, afegint un logo (en negatiu) al capçalera.</p>"
                "<p>La <strong>imatge especial</strong> s'utilitza com a miniatura en altres seccions de la web (categories relacionades i seleccions).</p>"
                "<p>Ten en compte que els canvis que realitzis aquí poden afectar la presentació de l'esdeveniment especial.</p>"
                "<p><em>Afegeix etiquetes (tags) rellevants per millorar el <strong>SEO</strong> de l'esdeveniment.</em></p>"
                "<p><em>La <strong>categoria</strong> és opcional; no obstant això, determinarà com es vincula l'esdeveniment. Per defecte, s'associarà a categories del tipus 'festes i tradicions'.</em></p>"
                "<p><strong>Nota:</strong> Abans d'eliminar un esdeveniment, comprova que realment no el necessitis. Recordeu que també es pot despublicar en lloc d'eliminar-lo.</p>"
                "<p><em>El codi QR es genera automàticament cada cop que es desa l'esdeveniment. Aquest codi sempre serà vàlid sempre que l'enllaç de l'esdeveniment no canvii, com per exemple: <strong>https://gaudeixcabrerademar.cat/s/ilturo</strong>.</em></p>"
                "<p><em>El codi QR mantindrà la seva validesa sempre que el 'slug' de l'esdeveniment no es modifiqui, cosa que només passaria si es creen esdeveniments nous amb el mateix nom.</em></p>"
                "<p><em><i>Si ets desenvolupador/a, no modifiquis el slug manualment o des del 'shell' del projecte, ja que els canvis es gestionen automàticament quan es desa l'esdeveniment des del formulari o a través de la funció 'save'.</i></em></p>"
            ),
        }),
        # Otras secciones de fieldsets aquí si es necesario
    ]

    inlines = [EventoFicheroInline, EventoEspecialGaleriaImagenInline]
    readonly_fields = ('display_qr_code','download_qr_code')

    def display_qr_code(self, obj):
        if obj.qr_code:
            return mark_safe(f'<img src="{obj.qr_code.url}" width="100" height="100" />')
        else:
            return "Sense codi QR"

    display_qr_code.allow_tags = True
    display_qr_code.short_description = 'Codi QR'

    def download_qr_code(self, obj):
        if obj.qr_code:
            # Obtenemos la ruta completa del archivo QR
            qr_path = obj.qr_code.path
            # Creamos un nombre de archivo para la descarga
            download_filename = os.path.basename(qr_path)
            # Creamos un enlace personalizado para la descarga
            download_link = f'<a href="{obj.qr_code.url}" download="{download_filename}">Baixar QR</a>'
            return mark_safe(download_link)
        else:
            return "Sense codi QR"
    
    download_qr_code.short_description = 'Baixar QR'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "categoria":
            kwargs["queryset"] = Categoria.objects.filter(tipo="festes_i_tradicions")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
