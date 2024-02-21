from django.contrib import admin
from ..models import PostImagen,PostGaleriaImagen,Post, Categoria, PostFichero
from multimedia_manager.models import Fichero
from multimedia_manager.models import Imagen
from django.db.models import Q
from ..models import Tag
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from core.utils import refresh_cache

from modeltranslation.admin import TranslationAdmin





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
                    Q(subcategoriabannerimagen__isnull=True),
                    Q(subcategoriagaleriaimagen__isnull=True),
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
                    Q(alerta__isnull=True),
                    Q(postimagen__isnull=True) | Q(postimagen__post__id=post_id)
                )
            kwargs['empty_label'] = 'Sense imatge associada'
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PostFicheroInline(admin.TabularInline):
    model = PostFichero
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'fichero':
            agenda_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                agenda_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Fichero.objects.filter(
                Q(postfichero__isnull=True) | Q(postfichero__post__id=agenda_id),
                Q(eventofichero__isnull=True),
                Q(pdfcollectionresoluciofichero__isnull =True),
                Q(pdfcollectionjustificaciofichero__isnull=True),
                Q(pdfcollectionconvocatoriafichero__isnull=True),
                Q(pdfcollectiontotesfichero__isnull = True),
                Q(pdfdiversidadfichero__isnull=True),
                Q(compradescubrefichero__isnull=True),
                Q(alerta__isnull=True)
            )
            kwargs['empty_label'] = 'Sin fichero asociado'

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
                    Q(subcategoriabannerimagen__isnull=True),
                    Q(subcategoriagaleriaimagen__isnull=True),
                    Q(alerta__isnull=True),
                    Q(eventoespecialgaleriaimagen__isnull=True),
                    Q(categoriabannerimagen__isnull=True),
                    Q(subblogimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True),
                    Q(postimagen__isnull=True),
                    Q(subbloggaleriaimagen__isnull=True),
                    Q(diversidadimagenbanner__isnull=True),
                    Q(compradescubrepasosimagen__isnull=True),
                    Q(compradescubreimagen__isnull=True),
                    Q(compradescubregaleriaimagen__isnull=True),
                    Q(postgaleriaimagen__isnull=True) | Q(postgaleriaimagen__post__id=post_id),
                )
            kwargs['empty_label'] = 'Sin imagen asociada'
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




class PostAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('titulo_ca', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('titulo', 'descripcion')
    inlines = [PostImagenInline, PostGaleriaImagenInline, PostFicheroInline]
    actions = ['refresh_cache']
    autocomplete_fields = ['categoria','subcategoria']
    filter_horizontal = ('tags',)

    fieldsets = [
        (None, {
            'fields': 
            [
                'titulo',
                'metatitulo',
                'descripcion',
                'metadescripcion',
                'categoria',
                'subcategoria',
                'publicado',
                'tags'
            ],
            'description': (
                "<p><strong>Aquesta és la pàgina d'edició d'un Post.</strong></p>"
                "<p><em><u>Un Post</u></em> és una entrada del blog que pot contenir diferents tipus de continguts. "
                "És recomanable que cada Post estigui associat a una <strong>Categoria</strong> de tipus <em>normal</em> per garantir "
                "un funcionament harmoniós i tenir els camps necessaris per a la visualització adequada. "
                "Per a altres tipus d'entrades com <em>Lloc</em>, <em>Agenda</em>, <em>Visita Guiada</em>, etc., és preferible utilitzar "
                "les classes corresponents.</em></p>"
                "<p>Assegura't de triar la <strong>Categoria</strong> correcta i de completar tots els camps necessaris "
                "per a la millor experiència de l'usuari.</p>"
                "<p><em><u>Per evitar errors,</u></em> hem limitat la selecció de <strong>Categoria</strong> només a aquelles de tipus <em>normal</em>. "
                "També és recomanable que cada <em>Post</em> tingui <strong>una imatge per al banner</strong> i <strong>tres imatges a la galeria</strong> "
                "per a una presentació visual completa.</p>"
                "<p><em>Assegura't d'afegir tags amb sentit per què es farà servir per al <strong> SEO</strong>.</em></p>"
                "<p><strong>Atenció:</strong> Si decideixes eliminar aquest <em>Post</em>, assegura't de revisar la <strong>Categoria</strong> "
                "parent perquè està relacionada amb aquest <em>Post</em>. L'eliminació de la <strong>Categoria</strong> parent pot afectar "
                "els <em>Posts</em> associats.</p>"
            ),
        }),
        # Resto de los fieldsets aquí si es necesario
    ]



    def get_queryset(self, request):
        # Obtener el queryset original
        queryset = super().get_queryset(request)
        
        # Filtrar los objetos de tipo Agenda
        queryset = queryset.exclude(agenda__isnull=False).exclude(visitaguiada__isnull=False).exclude(mappoint__isnull=False).exclude(ruta__isnull=False).exclude(alojamiento__isnull=False).exclude(restaurante__isnull=False)
        
        return queryset


    def refresh_cache(self, request, queryset):
        refresh_cache(request)
        self.message_user(request, "La memòria cau de la pàgina d'inici s'ha refrescat amb èxit.")
    
    refresh_cache.short_description = "Refrescar Caché"
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "categoria":
            kwargs["queryset"] = Categoria.objects.filter().exclude(tipo="noticies").exclude(tipo="agenda").exclude(tipo="senderisme")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
