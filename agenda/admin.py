from django.contrib import admin
from .models import Agenda, AgendaGaleriaImagen
from multimedia_manager.models import Imagen
from django.db.models import Q


class PostGaleriaImagenInline(admin.TabularInline):
    model = AgendaGaleriaImagen
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            # Obtener el ID del post actual
            agenda_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                agenda_id = request.resolver_match.kwargs['object_id']
            
            # Filtrar las imágenes disponibles para seleccionar
                kwargs['queryset'] = Imagen.objects.filter(
                    Q(agendagaleriaimagen__isnull=True) | Q(agendagaleriaimagen__agenda__id=agenda_id),
                    Q(categoriabannerimagen__isnull=True),
                    Q(subblogimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True),
                    Q(postimagen__isnull=True),
                    Q(postgaleriaimagen__isnull=True)
                )
            kwargs['empty_label'] = 'Sin imagen asociada'
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AgendaAdmin(admin.ModelAdmin):
    inlines = [PostGaleriaImagenInline]
    

admin.site.register(Agenda, AgendaAdmin)
