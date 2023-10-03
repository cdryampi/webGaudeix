from django.contrib import admin

# Register your models here.

from multimedia_manager.models import Fichero
from .models import EventoFichero, EventoEspecial, EventoEspecialGaleriaImagen
from django.db.models import Q
from multimedia_manager.models import Imagen
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from blog.models import Tag, Categoria


class EventoFicheroInline(admin.TabularInline):
    model = EventoFichero
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'fichero':
            evento_id = None
            if 'object_id' in request.resolver_match.kwargs:
                evento_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Fichero.objects.filter(
                Q(eventofichero__isnull=True) | Q(eventofichero__id=evento_id),
                Q(eventofichero__isnull=True), 
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
    filter_horizontal = ('agendas', 'videos', 'carruseles','tags')

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
                'agendas',
                'logo_especial',
                'imagen_especial',
                'tags',
                'parallax',
                'videos',
                'carruseles'
            ],
            'description': (
                "<p><strong>Aquesta és la pàgina d'edició d'un esdeveniment especial.</strong></p>"
                "<p><em>Els <u>esdeveniments especials</u> són una part auxiliar del lloc web i es poden crear tants com desitgis.</em></p>"
                "<p>Assegura't de completar els camps i de marcar l'opció <strong>publicat</strong> perquè es mostri destacat a la web. També pots afegir un<strong> logo especial</strong> si vols destacar encara més amb un logo (en negatiu) aquest esdeveniment al header (també s'ha d'afegir al header).</p>"
                "<p>La <strong>imatge de l'especial</strong> només es fa servir com a miniatura per altres seccions de la web (categories relacionades i seleccions).</p>"
                "<p>Tingues en compte que els canvis que facis aquí poden afectar la forma en què es presenta l'esdeveniment especial.</p>"
                "<p><em>Assegura't d'afegir tags amb sentit per què es farà servir per al <strong> SEO</strong>.</em></p>"
                "<p><em>La <strong>categoria</strong> és opcional, però això determinarà on es vincularà. En principi, es vincularà a una categoria de tipus 'festes i tradicions'.</em></p>"
                "<p><strong>Nota:</strong> Abans d'eliminar un esdeveniment, verifica que no el necessitis, ja que es pot despublicar.</p>"
            ),
        }),
        # Otras secciones de fieldsets aquí si es necesario
    ]

    inlines = [EventoFicheroInline, EventoEspecialGaleriaImagenInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "categoria":
            kwargs["queryset"] = Categoria.objects.filter(tipo="festes_i_tradicions")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
