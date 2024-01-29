from django.contrib import admin
from django.db.models import Q
from .models import Alerta
from multimedia_manager.models import Imagen, Fichero

# Register your models here.
@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_fin')
    list_filter = ('fecha_inicio', 'fecha_fin')
    search_fields = ('titulo', 'descripcion')
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'descripcion',
                'color',
                'fecha_inicio',
                'fecha_fin',
                'publicado',
                'fichero',
                'ver_mas',
                'imagen',
            ],
            'description': (
                "<p><strong>Gestió d'Alertes.</strong></p>"
                "<p><em>Aquesta secció permet la creació i modificació d'alertes per a esdeveniments o situacions importants en el lloc web.</em></p>"
                "<p>Aquestes alertes es poden utilitzar per informar als usuaris sobre canvis no planificats, esdeveniments urgents o qualsevol informació rellevant.</p>"
                "<p><em>Les alertes contenen informació detallada, incloent títol, descripció, dates d'inici i fi, i una imatge opcional.</em></p>"
                "<p><em>La prioritat per mostrar al botó de l'alerta es primer el fitxer PDF i després l'enllaç.</em></p>"
                "<p><strong>Nota:</strong> Assegura't que les dates d'inici i fi de l'alerta siguin correctes i que la descripció sigui clara i precisa.</p>"
                "<p><em>La imatge associada hauria de ser representativa del contingut de l'alerta per captar millor l'atenció dels usuaris.</em></p>"
            ),
        }),
        # Otras secciones de fieldsets aquí si es necesario
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            alerta = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                alerta = request.resolver_match.kwargs['object_id']
                kwargs['queryset'] = Imagen.objects.filter(
                    Q(subcategoriagaleriaimagen__isnull=True),
                    Q(subcategoriabannerimagen__isnull=True),
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
                    Q(compradescubreimagen__isnull=True),
                    Q(alerta__isnull=True) | Q(alerta = alerta)
                )

        if db_field.name == 'fichero':
            alerta = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                alerta = request.resolver_match.kwargs['object_id']

                kwargs['queryset'] = Fichero.objects.filter(
                    Q(postfichero__isnull=True),
                    Q(eventofichero__isnull=True),
                    Q(pdfcollectionresoluciofichero__isnull =True),
                    Q(pdfcollectionjustificaciofichero__isnull=True),
                    Q(pdfcollectionconvocatoriafichero__isnull=True),
                    Q(pdfcollectiontotesfichero__isnull = True),
                    Q(pdfdiversidadfichero__isnull=True),
                    Q(compradescubrefichero__isnull=True),
                    Q(alerta__isnull=True) | Q(alerta = alerta)
                )
        kwargs['empty_label'] = 'Sense fitxer associat'
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
