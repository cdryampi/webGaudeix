from django.contrib import admin

# Register your models here.

from multimedia_manager.models import Fichero
from .models import EventoFichero, EventoEspecial, EventoEspecialGaleriaImagen
from django.db.models import Q
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from multimedia_manager.models import Imagen

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
                Q(eventofichero__isnull=False) | Q(postfichero__isnull=True)
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
                    Q(eventoespecialgaleriaimagen__isnull=True) | Q(eventoespecialgaleriaimagen__evento_especial_id=evento_especial)
                )
            kwargs['empty_label'] = 'Sense imatge associada'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)





@admin.register(EventoEspecial)
class EventoEspecialAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_evento', 'publicado']
    list_filter = ['fecha_evento', 'publicado']
    search_fields = ['titulo']
    filter_horizontal = ('agendas', 'videos', 'carruseles')

    fieldsets = (
        ('Informació general', {
            'fields': ('titulo', 'fecha_evento', 'fecha_fin', 'descripcion_larga', 'descripcion_corta', 'logo_especial','color', 'publicado', 'metatitulo', 'metadescripcion')
        }),
        ('Vinculat a', {
            'fields': ('agendas', 'parallax', 'videos', 'carruseles')
        }),
    )
    inlines = [EventoFicheroInline, EventoEspecialGaleriaImagenInline]
