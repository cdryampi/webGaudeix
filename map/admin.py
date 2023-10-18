from .models import MapPoint
from django.contrib import admin
from blog.models import PostImagen, PostGaleriaImagen
from multimedia_manager.models import Imagen
from django.db.models import Q
from .utils import export_map_points_csv


class PostImagenInline(admin.TabularInline):
    model = PostImagen
    extra = 1
    readonly_fields = ['imagen_preview']

    def imagen_preview(self, instance):
        if instance.imagen:
            return instance.imagen.imagen_thumbnail()
        return '(Cap imatge associada)'

    imagen_preview.short_description = 'Imatge associada'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            post_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                post_id = request.resolver_match.kwargs['object_id']
                kwargs['queryset'] = Imagen.objects.filter(
                    Q(eventoespecialgaleriaimagen__isnull=True),
                    Q(categoriabannerimagen__isnull=True),
                    Q(subblogimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True),
                    Q(postgaleriaimagen__isnull=True),
                    Q(subbloggaleriaimagen__isnull=True),
                    Q(diversidadimagenbanner__isnull=True),
                    Q(compradescubrepasosimagen__isnull=True),
                    Q(compradescubreimagen__isnull=True),
                    Q(compradescubregaleriaimagen__isnull=True),
                    Q(postimagen__isnull=True) | Q(postimagen__post__id=post_id)
                )
            kwargs['empty_label'] = 'Sense imatge associada'
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class PostGaleriaImagenInline(admin.TabularInline):
    model = PostGaleriaImagen
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            # Obtener el ID del post actual
            post_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                post_id = request.resolver_match.kwargs['object_id']
            
            # Filtrar las imágenes disponibles para seleccionar
                kwargs['queryset'] = Imagen.objects.filter(
                    Q(eventoespecialgaleriaimagen__isnull=True),
                    Q(categoriabannerimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True),
                    Q(subblogimagen__isnull=True),
                    Q(subbloggaleriaimagen__isnull=True),
                    Q(postimagen__isnull=True),
                    Q(diversidadimagenbanner__isnull=True),
                    Q(compradescubrepasosimagen__isnull=True),
                    Q(compradescubreimagen__isnull=True),
                    Q(compradescubregaleriaimagen__isnull=True),
                    Q(postgaleriaimagen__isnull=True) | Q(postgaleriaimagen__post__id=post_id),
                )
            kwargs['empty_label'] = 'Sin imagen asociada'
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MapPointAdmin(admin.ModelAdmin):


    inlines = [PostImagenInline, PostGaleriaImagenInline]
    list_display = ('titulo', 'latitud', 'longitud', 'icono')
    list_filter = ('icono',)
    search_fields = ('titulo', 'latitud', 'longitud')
    autocomplete_fields = ['categoria']
    actions = [export_map_points_csv]
    
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'metatitulo',
                'descripcion',
                'metadescripcion',
                'publicado',
                'categoria',
                'latitud',
                'longitud',
                'icono',
                'calle',
                'enlace_google_maps',
            ],
            'description': (
                "<p><strong>Aquesta és la pàgina d'edició d'un Map Point.</strong></p>"
                "<p><em>Els <u>llocs(Map points)</u> són una part auxiliar del lloc web i es poden afegir totes les direccions que tinguin relació amb Cabrera de Mar.</em></p>"
                "<p>Assegura't de completar els camps i de marcar l'opció <strong>publicat</strong> perquè es mostri a la web.</p>"
                "<p>Pots tenir dos tipus d'imatges, el banner que surt la imatge petita al costat de la descripció i la galeria que pots posar totes les imatges que vols (és una galeria d'imatges a la part superior de la landing).</p>"
                "<p>Has de tenir en compte que les coordinades de latitud i longitud són les de Google Maps i pots afegir també un enllaç cap a la posició exacte o el sistema generarà una amb les coordenades.</p>"
                "<p>Tenim un camp opcional per afegir informació addicional a la part inferior del mapa, fes-ho servir com a advertiment o com vulguis.</p>"
                "<p><strong>Nota:</strong> Abans d'eliminar un Map Point, verifica que no el necessitis, ja que es pot despublicar i no afectar a les rutes de la categoria a senderisme si el tenim relacionat.</p>"
            ),
        }),
        # Otras secciones de fieldsets aquí si es necesario
    ]



admin.site.register(MapPoint, MapPointAdmin)
