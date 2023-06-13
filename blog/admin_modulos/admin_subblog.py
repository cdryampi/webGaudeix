from django.db import models
from django.contrib import admin
from personalizacion.models import CarruselSubBlog
from ..models import SubBlogImagen
from multimedia_manager.models import Imagen
from django.db.models import Q


# Se define una clase inline para mostrar imágenes de subblogs en línea en el admin
class SubBlogImagenInline(admin.TabularInline):
    model = SubBlogImagen
    extra = 1
    readonly_fields = ['imagen_preview']

    def imagen_preview(self, instance):
        if instance.imagen:
            return instance.imagen.imagen_thumbnail()
        return '(Cap imatge associada)'

    imagen_preview.short_description = 'Imatge associada'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            subblog_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                subblog_id = request.resolver_match.kwargs['object_id']
            kwargs['queryset'] = Imagen.objects.filter(
                Q(subblogimagen__isnull=True) | Q(subblogimagen__subblog_id=subblog_id),
                categoriabannerimagen__isnull=True,
                categoriagaleriaimagen__isnull=True,
                postimagen__isnull=True,
                postgaleriaimagen__isnull=True,
                agendagaleriaimagen__isnull=True,
                visitaguidadagaleriaimagen__isnull=True
            )
            kwargs['empty_label'] = 'Sense imatge associada'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class CarruselInLine(admin.StackedInline):
    model = CarruselSubBlog
    extra = 1
# Resto del código del admin de SubBlog
class SubBlogAdmin(admin.ModelAdmin):
    # Personalización del modelo en el administrador
    list_display = ('titulo', 'publicado', 'fecha_creacion', 'modificado_por')
    list_filter = ('publicado',)
    search_fields = ('titulo', 'contenido')
    inlines = [SubBlogImagenInline, CarruselInLine]
    fields = ['titulo', 'contenido', 'publicado', 'metatitulo', 'metadescripcion']
    
