from django.contrib import admin
from ..models import CategoriaBannerImagen, CategoriaGaleriaImagen
from multimedia_manager.models import Imagen
from django import forms
from django.db.models import Q


class CategoriaBannerImagenInline(admin.TabularInline):
    model = CategoriaBannerImagen
    extra = 1
    readonly_fields = ['imagen_preview']

    def imagen_preview(self, instance):
        if instance.imagen:
            return instance.imagen.imagen_thumbnail()
        return '(Cap imatge associada)'

    imagen_preview.short_description = 'Imatge associada'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            categoria_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                categoria_id = request.resolver_match.kwargs['object_id']
            kwargs['queryset'] = Imagen.objects.filter(
                Q(categoriabannerimagen__isnull=True) | Q(categoriabannerimagen__categoria_id=categoria_id),
                subblogimagen__isnull=True,
                categoriagaleriaimagen__isnull=True,
                postimagen__isnull=True,
                postgaleriaimagen__isnull = True,
                agendagaleriaimagen__isnull=True
            )
            kwargs['empty_label'] = 'Sense imatge associada'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Se define una clase inline para mostrar galería de imágenes de categorías en línea en el admin
# class CategoriaGaleriaImagenInline(admin.TabularInline):
#     model = CategoriaGaleriaImagen
class CategoriaGaleriaImagenInline(admin.TabularInline):
    model = CategoriaGaleriaImagen
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            categoria_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                categoria_id = request.resolver_match.kwargs['object_id']
                #print(categoria_id)
                kwargs['queryset'] = Imagen.objects.filter(
                    Q(categoriabannerimagen__isnull=True),
                    Q(subblogimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True) | Q(categoriagaleriaimagen__categoria_id=categoria_id),
                    Q(postimagen__isnull=True),
                    Q(postgaleriaimagen__isnull=True),
                    Q(agendagaleriaimagen__isnull=True)
                )
            kwargs['empty_label'] = 'Sense imatge associada'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Se define la configuración del admin para el modelo Categoria
class CategoriaAdmin(admin.ModelAdmin):
    
    list_display = ['titulo', 'especial', 'color']
    list_filter = ['especial']
    search_fields = ['titulo']
    inlines = [CategoriaBannerImagenInline,CategoriaGaleriaImagenInline]
    fields = ['titulo', 'especial', 'color', 'descripcion','publicado','subblog']
    # readonly_fields = ['color']
