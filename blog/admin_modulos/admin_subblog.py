from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from multimedia_manager.models import Imagen
from django.db.models import Q

from ..models import SubBlog, SubBlogImagen, SubblogGaleriaImagen

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
                subbloggaleriaimagen__isnull= True
            )
            kwargs['empty_label'] = 'Sense imatge associada'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class SubblogGaleriaImagenInline(admin.TabularInline):
    model = SubblogGaleriaImagen
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            subblog_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                subblog_id = request.resolver_match.kwargs['object_id']
                #print(categoria_id)
                kwargs['queryset'] = Imagen.objects.filter(
                    Q(categoriabannerimagen__isnull=True),
                    Q(subblogimagen__isnull=True),
                    Q(subbloggaleriaimagen__isnull=True) | Q(subbloggaleriaimagen__subblog_id=subblog_id),
                    Q(postimagen__isnull=True),
                    Q(postgaleriaimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True),
                )
            kwargs['empty_label'] = 'Sense imatge associada'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class SubBlogAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'publicado', 'fecha_creacion', 'modificado_por', 'preview_link')
    list_filter = ('publicado',)
    search_fields = ('titulo', 'contenido')
    inlines = [SubBlogImagenInline, SubblogGaleriaImagenInline]
    fields = ['titulo', 'contenido', 'publicado', 'metatitulo', 'metadescripcion']

    def preview_link(self, obj):
        if obj.id:
            url = reverse('blog:detalle-subblog', kwargs={'slug': obj.slug})
            return format_html('<a href="{}" target="_blank">Ver en el sitio</a>', url)
        return '-'

    preview_link.short_description = 'Vista previa'

