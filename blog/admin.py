from django.contrib import admin
from .models import Categoria
from django.utils.html import format_html
from django.forms import BaseInlineFormSet
from .models import SubBlog, Categoria, Fichero, Post, GaleriaImagenPost, SubBlogImagen, CategoriaBannerImagen, CategoriaGaleriaImagen
from multimedia_manager.models import Imagen
from django import forms
from dal import autocomplete
from django.utils.safestring import mark_safe

# Se define una clase inline para mostrar imágenes en línea en el admin
class ImagenInline(admin.TabularInline):
    model = Imagen
    extra = 1

# Se define una clase inline para mostrar imágenes de subblogs en línea en el admin
class SubBlogImagenInline(admin.TabularInline):
    model = SubBlogImagen
    extra = 1
    model = SubBlogImagen
    extra = 1
    readonly_fields = ['imagen_preview']

    def imagen_preview(self, instance):
        if instance.imagen:
            return instance.imagen.imagen_thumbnail()
        return '(Ninguna imagen asociada)'

    imagen_preview.short_description = 'Imagen asociada'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            subblog_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                subblog_id = request.resolver_match.kwargs['object_id']
            kwargs['queryset'] = Imagen.objects.filter(subblogimagen__isnull=True) | Imagen.objects.filter(subblogimagen__subblog_id=subblog_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Se define una clase inline para mostrar imágenes de categorías en línea en el admin
class CategoriaBannerImagenInline(admin.TabularInline):
    model = CategoriaBannerImagen
    inlines = [ImagenInline]

# Se define una clase inline para mostrar galería de imágenes de categorías en línea en el admin
class CategoriaGaleriaImagenInline(admin.TabularInline):
    model = CategoriaGaleriaImagen

# Se define la configuración del admin para el modelo SubBlog
class SubBlogAdmin(admin.ModelAdmin):
    # Personalización del modelo en el administrador
    list_display = ('titulo', 'publicado', 'fecha_creacion', 'modificado_por')
    list_filter = ('publicado',)
    search_fields = ('titulo', 'contenido')
    inlines = [SubBlogImagenInline]


# Se define la configuración del admin para el modelo Categoria
class CategoriaAdmin(admin.ModelAdmin):

    inlines = [CategoriaBannerImagenInline, CategoriaGaleriaImagenInline]
    search_fields = ['titulo', 'subtitulo'] 

# Se registra el modelo Categoria en el admin con su configuración
admin.site.register(Categoria, CategoriaAdmin)

# Se registra el modelo SubBlog en el admin con su configuración
admin.site.register(SubBlog, SubBlogAdmin)
