from django.contrib import admin
from .models import Subvencion, SubvencionDescripcion
from .models import PDFCollectionConvocatoriaFichero, PDFCollectionJustificacioFichero, PDFCollectionResolucioFichero, PDFCollectionTotesFichero
from multimedia_manager.models import Fichero
from django.db.models import Q

# Register your models here.

class PDFCollectionConvocatoriaFicheroInline(admin.TabularInline):
    model = PDFCollectionConvocatoriaFichero
    extra = 1

    verbose_name_plural = "Fitxers PDF de la Convocatòria"
    verbose_name = "Fitxer PDF de la Convocatòria"
    help_text = "Aquí podeu pujar fitxers PDF relacionats amb la convocatòria de subvenció."


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'fichero':
            subvencion_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                subvencion_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Fichero.objects.filter(
                Q(pdfcollectionconvocatoriafichero__isnull=True) | Q(pdfcollectionconvocatoriafichero__subvencion__id=subvencion_id),
                Q(eventofichero__isnull=True),
                Q(postfichero__isnull=True),
                Q(pdfcollectionjustificaciofichero__isnull=True),
                Q(pdfcollectionresoluciofichero__isnull =True),
                Q(pdfcollectiontotesfichero__isnull = True),
                Q(pdfdiversidadfichero__isnull=True),
                Q(compradescubrefichero__isnull=True),
                Q(alerta__isnull=True)
            )
            kwargs['empty_label'] = 'Sin fichero asociado'
            kwargs['help_text'] = 'Selecciona un fitxer PDF associat a aquesta convocatòria de subvenció.'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PDFCollectionJustificacioFicheroInline(admin.TabularInline):
    model = PDFCollectionJustificacioFichero
    extra = 1

    verbose_name_plural = "Fitxers PDF de la Justificació"
    verbose_name = "Fitxer PDF de la Justificació"
    help_text = "Aquí podeu pujar fitxers PDF relacionats amb la Justificació de subvenció."


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'fichero':
            subvencion_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                subvencion_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Fichero.objects.filter(
                Q(pdfcollectionjustificaciofichero__isnull=True) | Q(pdfcollectionjustificaciofichero__subvencion__id=subvencion_id),
                Q(pdfcollectionconvocatoriafichero__isnull=True),
                Q(pdfcollectiontotesfichero__isnull = True),
                Q(eventofichero__isnull=True),
                Q(postfichero__isnull=True),
                Q(pdfcollectionresoluciofichero__isnull =True),
                Q(pdfdiversidadfichero__isnull=True),
                Q(compradescubrefichero__isnull=True),
                Q(alerta__isnull=True)
            )
            kwargs['empty_label'] = 'Sin fichero asociado'
            kwargs['help_text'] = 'Selecciona un fitxer PDF associat a aquesta convocatòria de subvenció.'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PDFCollectionResolucioFicheroInline(admin.TabularInline):
    model = PDFCollectionResolucioFichero
    extra = 1

    verbose_name_plural = "Fitxers PDF de la resolució"
    verbose_name = "Fitxer PDF de la resolució"
    help_text = "Aquí podeu pujar fitxers PDF relacionats amb la resolució de subvenció."


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'fichero':
            subvencion_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                subvencion_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Fichero.objects.filter(
                Q(pdfcollectionresoluciofichero__isnull =True) | Q(pdfcollectionresoluciofichero__subvencion__id=subvencion_id),
                Q(pdfcollectionjustificaciofichero__isnull=True),
                Q(pdfcollectionconvocatoriafichero__isnull=True),
                Q(pdfcollectiontotesfichero__isnull = True),
                Q(eventofichero__isnull=True),
                Q(postfichero__isnull=True),
                Q(pdfdiversidadfichero__isnull=True),
                Q(compradescubrefichero__isnull=True),
                Q(alerta__isnull=True)
            )
            kwargs['empty_label'] = 'Sin fichero asociado'
            kwargs['help_text'] = 'Selecciona un fitxer PDF associat a aquesta resolució de subvenció.'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PDFCollectionTotesFicheroInline(admin.TabularInline):
    model = PDFCollectionTotesFichero
    extra = 1

    verbose_name_plural = "Fitxers PDF de tot"
    verbose_name = "Fitxer PDF o zip per aquesta subvenció"
    help_text = "Aquí podeu pujar fitxers PDF o zip relacionats amb aquesta subvenció."


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'fichero':
            subvencion_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                subvencion_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Fichero.objects.filter(
                Q(pdfcollectiontotesfichero__isnull = True) | Q(pdfcollectiontotesfichero__subvencion__id=subvencion_id),
                Q(pdfcollectionresoluciofichero__isnull = True),
                Q(pdfcollectionjustificaciofichero__isnull = True),
                Q(pdfcollectionconvocatoriafichero__isnull = True), 
                Q(eventofichero__isnull=True),
                Q(postfichero__isnull=True),
                Q(pdfdiversidadfichero__isnull=True),
                Q(compradescubrefichero__isnull=True),
                Q(alerta__isnull=True)
            )
            kwargs['empty_label'] = 'Sin fichero asociado'
            kwargs['help_text'] = 'Selecciona un fitxer PDF o zip associat a aquesta subvenció.'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)





class SubvencionAdmin(admin.ModelAdmin):
    inlines = [PDFCollectionConvocatoriaFicheroInline, PDFCollectionJustificacioFicheroInline, PDFCollectionResolucioFicheroInline, PDFCollectionTotesFicheroInline]
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'descripcion',
                'disclaimer',
                'publicado'
            ],
            'description': (
                "<p><strong><em>Administració de Subvencions</em></strong></p>"
                "<p>Aquesta secció permet afegir, modificar i esborrar les subvencions. Es poden gestionar tots els detalls rellevants de cada subvenció, incloent títol, descripció, imatge i disclaimers.</p>"
                "<p>Utilitza el camp <em>disclaimer</em> per a afegir informació addicional o advertències importants relacionades amb la subvenció.</p>"
                "<p>Recorda que aquesta secció forma part integral de la gestió de contingut de la web, especialment en àrees relacionades amb la cultura i festes.</p>"
                "<p>Tingues en compte que la informació introduïda aquí tindrà un impacte directe en com les subvencions són presentades i gestionades en el lloc web.</p>"
            ),
        }),
        # Resto de los fieldsets
    ]

class SubvencionDescripcionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'descripcion',
                'imagen',
                'disclaimer',
            ],
            'description': (
                "<p><strong><em>Administració de la Descripció General de Subvencions</em></strong></p>"
                "<p>Aquesta secció permet configurar la descripció general que apareixerà en la secció de subvencions del lloc web. És un lloc centralitzat per gestionar la informació que es mostra en totes les subvencions.</p>"
                "<p>Assegura't de proporcionar un títol atractiu, una descripció detallada, i seleccionar una imatge representativa per a la secció de subvencions.</p>"
                "<p>El camp <em>disclaimer</em> pot ser utilitzat per a afegir qualsevol informació addicional o advertències generals rellevants per a totes les subvencions.</p>"
                "<p>Aquesta configuració afectarà la presentació general de les subvencions en el lloc web, així que és important mantenir-la actualitzada i precisa.</p>"
            ),
        }),
        # Resto de los fieldsets
    ]

admin.site.register(Subvencion, SubvencionAdmin)
admin.site.register(SubvencionDescripcion, SubvencionDescripcionAdmin)