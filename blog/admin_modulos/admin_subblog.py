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
                subcategoriabannerimagen__isnull=True,
                subcategoriagaleriaimagen__isnull=True,
                categoriabannerimagen__isnull=True,
                categoriagaleriaimagen__isnull=True,
                postimagen__isnull=True,
                postgaleriaimagen__isnull=True,
                subbloggaleriaimagen__isnull= True,
                eventoespecialgaleriaimagen__isnull=True,
                diversidadimagenbanner__isnull=True,
                compradescubrepasosimagen__isnull=True,
                compradescubreimagen__isnull=True,
                compradescubregaleriaimagen__isnull=True,
                alerta__isnull=True
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
                    Q(eventoespecialgaleriaimagen__isnull=True),
                    Q(diversidadimagenbanner__isnull=True),
                    Q(compradescubrepasosimagen__isnull=True),
                    Q(compradescubreimagen__isnull=True),
                    Q(compradescubregaleriaimagen__isnull=True),
                    Q(alerta__isnull=True),
                    Q(subcategoriagaleriaimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True),
                    Q(subcategoriabannerimagen__isnull=True),
                )
            kwargs['empty_label'] = 'Sense imatge associada'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class SubBlogAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'publicado', 'fecha_creacion', 'modificado_por', 'preview_link')
    list_filter = ('publicado',)
    search_fields = ('titulo', 'contenido')
    inlines = [SubBlogImagenInline, SubblogGaleriaImagenInline]
    filter_horizontal = ('tags',)
    
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'contenido',
                'publicado',
                'metatitulo',
                'metadescripcion',
                'tags'
            ],
            'description': (
                "<p><strong>Aquesta és la pàgina d'edició d'un SubBlog.</strong></p>"
                "<p><em>Un SubBlog és una entitat principal del lloc web que serveix per agrupar diversos tipus de continguts com Post, Agendes, Visites Guiades, Rutes de Senderisme i altres. Aquesta agrupació permet organitzar i presentar diferents elements relacionats sota un mateix tema o categoria.</em></p>"
                "<p><em>Si decideixes <strong>despublicar</strong> aquest SubBlog, els continguts associats deixaran de ser visibles per als usuaris i no es mostrarà als visitants del lloc. Tingues en compte que això pot afectar altres parts de la web que utilitzen aquesta agrupació.</em></p>"
                "<p><em>Assegura't de revisar la configuració del <strong>Header</strong> o <strong>HeaterFooter</strong> de la app de Header per garantir que aquest SubBlog no es mostri si és el que interessa. Recorda que els canvis aquí realitzats poden afectar la manera en què es mostra el SubBlog i els continguts associats a la web.</em></p>"
                "<p><em>Assegura't d'afegir tags amb sentit per què es farà servir per al <strong> SEO</strong>.</em></p>"
            ),
        }),
        # Otras secciones de fieldsets aquí si es necesario
    ]

    def preview_link(self, obj):
        if obj.id:
            url = reverse('blog:detalle-subblog', kwargs={'slug': obj.slug})
            return format_html('<a href="{}" target="_blank">Anar a veure el lloc</a>', url)
        return '-'

    preview_link.short_description = 'Vista previa'

