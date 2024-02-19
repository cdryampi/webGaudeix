from django.contrib import admin

# Register your models here.
from modeltranslation.admin import TranslationAdmin
from multimedia_manager.models import Fichero
from .models import EventoFichero, EventoEspecial, EventoEspecialGaleriaImagen, MedidaEconomica, Autor, Mensaje, EventoMensaje
from django.db.models import Q
from multimedia_manager.models import Imagen
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from blog.models import Tag, Categoria
from django.http import HttpResponse
from django.http import FileResponse
import os
from django.utils.safestring import mark_safe


class MensajeAdmin(TranslationAdmin, admin.ModelAdmin):
    model = Mensaje
    fieldsets = [
        (None, {
            'fields': [
                'autor',
                'nombre_interno',
                'titulo',
                'contenido',
                'mensaje_despedida'
            ],
            'description': (
                "<p>Aquesta és la pàgina d'administració dels missatges.</p>"
                "<p>Aquí pots gestionar els missatges individuals que es vinculen amb els esdeveniments especials.</p>"
                "<p>Cada missatge ara inclou un títol, que pot ser una frase o una declaració impactant com 'Dies de família, dies de poble' o 'Les entitats, pilar fonamental de Nadal'.</p>"
                "<p>A més, pots afegir un missatge de comiat personalitzat a cada missatge, com 'Bon Nadal' o 'Bon Nadal i feliç 2023!', per donar un toc final més càlid i proper.</p>"
                "<p>Recorda que és important mantenir els missatges actuals, pertinents i ben redactats, reflectint adequadament l'essència de cada esdeveniment especial.</p>"
                "<p>Aquesta interfície et permet gestionar fàcilment aquesta informació, assegurant que tots els detalls dels missatges estiguin ben presentats.</p>"
                "<p>No oblidis guardar els canvis després de realitzar qualsevol actualització o modificació en els missatges.</p>"
            ),
        }),
    ]


class MedidaEconomicaAdmin(TranslationAdmin, admin.ModelAdmin):
    model = MedidaEconomica
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'titulo_html',
                'descripcion',
                'impacto_economico',
                'publicado'
            ],
            'description': (
                "<p>Mesures econòmiques per l'esdeveniment especials pensat pel programa d'estabilització econòmica sostenible.</p>"
                "<p>En aquest model pots afegir les mesures que vols.</p>"
                "<p>Aquest model el fem servir el popup que explica les mesures d'estalvi o d'altres tipus.</p>"
            ),
        }),
    ]


class EventoFicheroInline(admin.TabularInline):
    model = EventoFichero
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'fichero':
            evento_id = None
            if 'object_id' in request.resolver_match.kwargs:
                evento_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Fichero.objects.filter(
                Q(eventofichero__isnull=True) | Q(eventofichero__evento_id=evento_id),
                Q(postfichero__isnull=True),
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
                    Q(subcategoriagaleriaimagen__isnull=True),
                    Q(subcategoriabannerimagen__isnull=True),
                    Q(alerta__isnull=True),
                    Q(categoriabannerimagen__isnull=True),
                    Q(subblogimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True),
                    Q(postimagen__isnull=True),
                    Q(postgaleriaimagen__isnull=True),
                    Q(subbloggaleriaimagen__isnull=True),
                    Q(diversidadimagenbanner__isnull=True),
                    Q(compradescubrepasosimagen__isnull=True),
                    Q(compradescubreimagen__isnull=True),
                    Q(compradescubregaleriaimagen__isnull=True),
                    Q(eventoespecialgaleriaimagen__isnull=True) | Q(eventoespecialgaleriaimagen__evento_especial_id=evento_especial)
                )
            kwargs['empty_label'] = 'Sense imatge associada'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)





class EventoMensajeAdmin(admin.ModelAdmin):
    model = EventoMensaje
    fieldsets = [
        (None, {
            'fields': [
                'evento_especial',
                'mensaje',
            ],
            'description': (
                "<p>Aquesta és la pàgina d'edició d'un missatge vinculat.</p>"
                "<p>En aquest model pots vincular els missatges amb l'esdeveniment especial.</p>"
                "<p>S'ha pensat per afegir les paraules del batlle/alcade i pels regidors, permetent una gestió centralitzada i organitzada dels missatges clau de l'event.</p>"
                "<p>Aquí pots seleccionar l'esdeveniment al qual pertany el missatge i l'autor del mateix. Això et permetrà crear una cronologia de missatges i comunicacions relacionades amb l'esdeveniment.</p>"
                "<p>Utilitza aquesta interfície per gestionar eficaçment els missatges i assegurar-te que tota la informació important està accessible i ben organitzada per a l'esdeveniment especial.</p>"
                "<p>Recorda guardar els canvis després de fer qualsevol modificació.</p>"
            ),
        }),
    ]


class AutorAdmin(TranslationAdmin, admin.ModelAdmin):
    model = Autor
    fieldsets = [
        (None, {
            'fields': [
                'nombre',
                'cargo',
                'foto',
            ],
            'description': (
                "<p>Aquesta és la pàgina d'administració dels autors.</p>"
                "<p>Aquí pots gestionar la informació dels autors dels missatges associats als esdeveniments especials.</p>"
                "<p>Cada autor pot ser un batlle, un alcalde, un regidor, o qualsevol altra figura destacada que contribueixi amb paraules o discursos a l'esdeveniment.</p>"
                "<p>En aquesta secció, pots afegir, editar o eliminar la informació dels autors, incloent el seu nom, càrrec i una foto opcional.</p>"
                "<p>És important mantenir aquesta informació actualitzada i precisa, ja que ajuda a contextualitzar els missatges i aporta un toc personal a l'esdeveniment especial.</p>"
                "<p>Aquesta interfície facilita la gestió dels autors, assegurant-te que cada missatge tingui la seva corresponent veu autèntica i reconeguda.</p>"
                "<p>Recorda guardar els canvis després de realitzar les modificacions necessàries.</p>"
            ),
        }),
    ]




class EventoMensajeInline(admin.TabularInline):
    model = EventoMensaje
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "mensaje":
            evento_especial_id = request.resolver_match.kwargs.get('object_id')
            if evento_especial_id:
                # Filtra los mensajes que no están vinculados a un evento especial o están vinculados al evento especial actual.
                kwargs["queryset"] = Mensaje.objects.filter(
                    Q(eventomensaje__isnull=True) |
                    Q(eventomensaje__evento_especial_id=evento_especial_id)
                )
            else:
                # Filtra los mensajes que no están vinculados a ningún evento especial.
                kwargs["queryset"] = Mensaje.objects.filter(eventomensaje__isnull=True)
            kwargs['empty_label'] = 'Sense missatge associat'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



@admin.register(EventoEspecial)
class EventoEspecialAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ['titulo', 'fecha_evento', 'publicado']
    list_filter = ['fecha_evento', 'publicado']
    search_fields = ['titulo']
    filter_horizontal = ('agendas', 'videos','tags')

    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'metatitulo',
                'descripcion_corta',
                'descripcion_larga',
                'metadescripcion',
                'fecha_evento',
                'fecha_fin',
                'publicado',
                'medida_economica',
                'categoria',
                'color',
                'mostrar_ahorro',
                'parallax',
                'display_qr_code',
                'download_qr_code',
                'agendas',
                'logo_especial',
                'imagen_especial',
                'tags',
                'videos',
            ],
            'description': (
                "<p><strong>Aquesta és la pàgina d'edició d'un esdeveniment especial.</strong></p>"
                "<p><em>Els <u>esdeveniments especials</u> són una part auxiliar del lloc web i pots crear-ne tants com desitgis.</em></p>"
                "<p>Assegura't de completar tots els camps i de marcar l'opció <strong>publicat</strong> perquè l'esdeveniment aparegui destacat a la web. També pots afegir un <strong>logo especial</strong> per destacar l'esdeveniment encara més, afegint un logo (en negatiu) al capçalera.</p>"
                "<p>La <strong>imatge especial</strong> s'utilitza com a miniatura en altres seccions de la web (categories relacionades i seleccions).</p>"
                "<p>Ten en compte que els canvis que realitzis aquí poden afectar la presentació de l'esdeveniment especial.</p>"
                "<p><em>Afegeix etiquetes (tags) rellevants per millorar el <strong>SEO</strong> de l'esdeveniment.</em></p>"
                "<p><em>La <strong>categoria</strong> és opcional; no obstant això, determinarà com es vincula l'esdeveniment. Per defecte, s'associarà a categories del tipus 'festes i tradicions'.</em></p>"
                "<p><strong>Nota:</strong> Abans d'eliminar un esdeveniment, comprova que realment no el necessitis. Recordeu que també es pot despublicar en lloc d'eliminar-lo.</p>"
                "<p><em>El codi QR es genera automàticament cada cop que es desa l'esdeveniment. Aquest codi sempre serà vàlid sempre que l'enllaç de l'esdeveniment no canvii, com per exemple: <strong>https://gaudeixcabrerademar.cat/s/ilturo</strong>.</em></p>"
                "<p><em>El codi QR mantindrà la seva validesa sempre que el 'slug' de l'esdeveniment no es modifiqui, cosa que només passaria si es creen esdeveniments nous amb el mateix nom.</em></p>"
                "<p><em><i>Si ets desenvolupador/a, no modifiquis el slug manualment o des del 'shell' del projecte, ja que els canvis es gestionen automàticament quan es desa l'esdeveniment des del formulari o a través de la funció 'save'.</i></em></p>"
            ),
        }),
        # Otras secciones de fieldsets aquí si es necesario
    ]

    inlines = [EventoFicheroInline, EventoEspecialGaleriaImagenInline, EventoMensajeInline]
    readonly_fields = ('display_qr_code','download_qr_code')

    def display_qr_code(self, obj):
        if obj.qr_code:
            return mark_safe(f'<img src="{obj.qr_code.url}" width="100" height="100" />')
        else:
            return "Sense codi QR"

    display_qr_code.allow_tags = True
    display_qr_code.short_description = 'Codi QR'

    def download_qr_code(self, obj):
        if obj.qr_code:
            # Obtenemos la ruta completa del archivo QR
            qr_path = obj.qr_code.path
            # Creamos un nombre de archivo para la descarga
            download_filename = os.path.basename(qr_path)
            # Creamos un enlace personalizado para la descarga
            download_link = f'<a href="{obj.qr_code.url}" download="{download_filename}">Baixar QR</a>'
            return mark_safe(download_link)
        else:
            return "Sense codi QR"
    
    download_qr_code.short_description = 'Baixar QR'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "categoria":
            kwargs["queryset"] = Categoria.objects.filter(tipo="festes_i_tradicions")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(MedidaEconomica, MedidaEconomicaAdmin)
admin.site.register(Mensaje, MensajeAdmin)
admin.site.register(Autor, AutorAdmin)