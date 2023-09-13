from django.contrib import admin
from ..models import CategoriaBannerImagen, CategoriaGaleriaImagen
from multimedia_manager.models import Imagen
from django import forms
from django.db.models import Q
from core.utils import refresh_cache

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
                subbloggaleriaimagen__isnull=True,
                eventoespecialgaleriaimagen__isnull=True
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
                    Q(eventoespecialgaleriaimagen__isnull=True),
                    Q(categoriabannerimagen__isnull=True),
                    Q(subblogimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True) | Q(categoriagaleriaimagen__categoria_id=categoria_id),
                    Q(postimagen__isnull=True),
                    Q(postgaleriaimagen__isnull=True),
                    Q(subbloggaleriaimagen__isnull=True),
                )
            kwargs['empty_label'] = 'Sense imatge associada'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



# Se define la configuración del admin para el modelo Categoria
class CategoriaAdmin(admin.ModelAdmin):
    
    list_display = ['titulo', 'especial', 'color']
    list_filter = ['especial']
    search_fields = ['titulo']
    inlines = [CategoriaBannerImagenInline,CategoriaGaleriaImagenInline]
    actions = ['refresh_cache']
    autocomplete_fields = ['subblog']
    search_fields = ['tags']
    fieldsets = [
        (None, {
            'fields': ['titulo', 'metatitulo', 'subtitulo', 'descripcion', 'metadescripcion', 'especial', 'tipo', 'color', 'publicado', 'subblog','tags'],
            'description': (
                "<p><strong>Aquesta és la pàgina d'edició d'una Categoria.</strong></p>"
                "<p><em>Les <u>Categories</u> són una part crítica del lloc web, ja que determinen la manera com els continguts relacionats es mostraran als usuaris. Pots utilitzar <strong>Categories</strong> per organitzar i categoritzar els continguts sota temes o categories específiques, com ara <em>Post</em>, <em>Agendes</em>, <em>Visites Guiades</em> i més.</em></p>"
                "<p>Assegura't que la categoria està <strong>publicada</strong> perquè es mostri a la llista de categories disponibles als usuaris. També pots marcar-la com <strong>Especial</strong> si vols donar-li una destacada a aquesta categoria.</p>"
                "<p>El <strong>Tipus</strong> que triïs limitarà la forma com veuràs el contingut, ja que cada tipus té una plantilla diferent. Això afectarà quins tipus de <em>Post</em> relacionats a aquesta categoria utilitzarem.</p>"
                "<p>Recorda que només pots tenir una Categoria del tipus <strong>Agenda</strong>. Si vols tenir-ne una altra per altres motius, pots fer-ho, però el sistema només detectarà la primera <em>Categoria Agenda</em> publicada.</p>"
                "<p>Si la categoria és <strong>Especial</strong>, apareixerà al principi amb un icono en blanc i fons transparent per mantenir el disseny.</p>"
                "<p>La <strong>imatge del Banner</strong> només és vàlida si s'utilitza la categoria especial. Totes les categories utilitzen la primera imatge de la galeria per a les miniatures.</p>"
                "<p>Recorda que els canvis que realitzis aquí poden afectar la forma en què es presenta la categoria i els continguts relacionats al lloc web.</p>"
                "<p><em>Assegura't d'afegir tags amb sentit per què es farà servir per al <strong> SEO</strong>.</em></p>"
                "<p><strong>Atenció:</strong> Quan vulguis eliminar una Categoria, revisa altres elements <strong> fills com entrades, visites guiades, etc</strong> per evitar errors, ja estan relacionats i no poden estar sense categoria i s'eliminará.</p>"
            ),
        }),
        # Otras secciones de fieldsets aquí si es necesario
    ]

    def refresh_cache(self, request, queryset):
        refresh_cache(request)
        self.message_user(request, "La memòria cau de la pàgina d'inici s'ha refrescat amb èxit.")

    refresh_cache.short_description = "Refrescar Caché"


