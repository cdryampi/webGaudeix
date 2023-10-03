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
                Q(compadescubrefichero__isnull=True),
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
                Q(compadescubrefichero__isnull=True),
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
                Q(compadescubrefichero__isnull=True),
            )
            kwargs['empty_label'] = 'Sin fichero asociado'
            kwargs['help_text'] = 'Selecciona un fitxer PDF o zip associat a aquesta subvenció.'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)





class SubvencionAdmin(admin.ModelAdmin):
    inlines = [PDFCollectionConvocatoriaFicheroInline, PDFCollectionJustificacioFicheroInline, PDFCollectionResolucioFicheroInline, PDFCollectionTotesFicheroInline]

admin.site.register(Subvencion, SubvencionAdmin)
admin.site.register(SubvencionDescripcion)