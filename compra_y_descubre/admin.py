from django.contrib import admin
from multimedia_manager.models import Fichero
from .models import CompraDescubre, CompraDescubreFichero, CompraDescubrePasosImagen, CompraDescubreImagen, CompraDescubreGaleriaImagen, EntidadComprayParticipa
from django.db.models import Q
from multimedia_manager.models import Imagen
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from blog.models import Tag, Categoria
# Register your models here.

class CompraDescubreFicheroInline(admin.TabularInline):
    model = CompraDescubreFichero
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'fichero':
            evento_id = None
            if 'object_id' in request.resolver_match.kwargs:
                evento_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Fichero.objects.filter(
                Q(compradescubrefichero__isnull=True) | Q(compradescubrefichero__id= evento_id),
                Q(eventofichero__isnull=True),
                Q(postfichero__isnull=True),
                Q(pdfcollectionresoluciofichero__isnull =True),
                Q(pdfcollectionjustificaciofichero__isnull=True),
                Q(pdfcollectionconvocatoriafichero__isnull=True),
                Q(pdfcollectiontotesfichero__isnull = True),
                Q(pdfdiversidadfichero__isnull=True)
            )
            kwargs['empty_label'] = 'Sin fichero asociado'

        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class CompraDescubrePasosImagenInline(admin.TabularInline):
    model = CompraDescubrePasosImagen
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
                    Q(eventoespecialgaleriaimagen__isnull=True),
                    Q(compradescubreimagen__isnull=True),
                    Q(compradescubregaleriaimagen__isnull=True),
                    Q(compradescubrepasosimagen__isnull=True) | Q(compradescubrepasosimagen__compradescubre_id=evento_especial)
                    )
            kwargs['empty_label'] = 'Sense imatge associada'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




class CompraDescubreGaleriaImagenInline(admin.TabularInline):
    model = CompraDescubreGaleriaImagen
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
                    Q(eventoespecialgaleriaimagen__isnull=True),
                    Q(compradescubreimagen__isnull=True),
                    Q(compradescubrepasosimagen__isnull=True),
                    Q(compradescubregaleriaimagen__isnull=True) | Q(compradescubregaleriaimagen__compradescubre_id=evento_especial)
                    )
            kwargs['empty_label'] = 'Sense imatge associada'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class CompraDescubreImagenInline(admin.TabularInline):
    model = CompraDescubreImagen
    extra = 1
    readonly_fields = ['imagen_preview']

    def imagen_preview(self, instance):
        if instance.imagen:
            return instance.imagen.imagen_thumbnail()
        return '(Cap imatge associada)'

    imagen_preview.short_description = 'Imatge associada'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            evento_especial = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                evento_especial = request.resolver_match.kwargs['object_id']
                kwargs['queryset'] = Imagen.objects.filter(
                    Q(eventoespecialgaleriaimagen__isnull=True),
                    Q(categoriabannerimagen__isnull=True),
                    Q(subblogimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True),
                    Q(postgaleriaimagen__isnull=True),
                    Q(subbloggaleriaimagen__isnull=True),
                    Q(diversidadimagenbanner__isnull=True),
                    Q(postimagen__isnull=True),
                    Q(compradescubrepasosimagen__isnull=True),
                    Q(compradescubregaleriaimagen__isnull=True),
                    Q(compradescubreimagen__isnull=True) | Q(compradescubreimagen__compradescubre_id = evento_especial)
                )
            kwargs['empty_label'] = 'Sense imatge associada'
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



@admin.register(CompraDescubre)
class CompraDescubreAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_inicio', 'publicado']
    list_filter = ['fecha_inicio', 'publicado']
    search_fields = ['titulo']
    filter_horizontal = ('tags','entidades')


    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'metatitulo',
                'descripcion_corta',
                'descripcion_larga',
                'metadescripcion',
                'fecha_inicio',
                'fecha_fin',
                'publicado',
                'primary_color',
                'secondary_color',
                'participante',
                'comerciante',
                'tags',
                'entidades',
                'sorteo'
            ],
            'description': (
                "<p><strong>Aquesta és la pàgina d'edició d'un esdeveniment Compra i descobreix.</strong></p>"
                "<p><em>Els <u>esdeveniments 'Compra i descobreix'</u> són una part auxiliar del lloc web i es poden crear tants com desitgis, es clar tantes com edicions que fa xarxabarris.</em></p>"
                "<p>Tingues en compte la duarada del programa, normalment es durant el mes del juny.</p>"
                "<p><em>Assegura't d'afegir tags amb sentit per què es farà servir per al <strong> SEO</strong>.</em></p>"
                "<p><em>La <strong>categoria</strong> és opcional, però això determinarà on es vincularà. En aquest cas no cal que tingui res vinculat.</em></p>"
                "<p><strong>Nota:</strong> Abans d'eliminar un esdeveniment 'Compra i descobreix', verifica que no el necessitis, ja que es pot despublicar i tenir un altre .</p>"
            ),
        }),
        # Otras secciones de fieldsets aquí si es necesario
    ]

    inlines = [CompraDescubrePasosImagenInline, CompraDescubreImagenInline, CompraDescubreFicheroInline, CompraDescubrePasosImagenInline, CompraDescubreGaleriaImagenInline]


@admin.register(EntidadComprayParticipa)
class EntidadComprayParticipaAdmin(admin.ModelAdmin):
    pass