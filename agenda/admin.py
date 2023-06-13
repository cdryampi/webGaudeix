from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Q
from multimedia_manager.models import Imagen
from .models import Agenda, AgendaGaleriaImagen, VisitaGuidada, VisitaGuidadaGaleriaImagen
from map.models import MapPoint
from django.forms import DurationField
from django import forms


class PostGaleriaImagenInline(admin.TabularInline):
    model = AgendaGaleriaImagen
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            agenda_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                agenda_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Imagen.objects.filter(
                Q(agendagaleriaimagen__isnull=True) | Q(agendagaleriaimagen__agenda__id=agenda_id),
                Q(categoriabannerimagen__isnull=True),
                Q(subblogimagen__isnull=True),
                Q(categoriagaleriaimagen__isnull=True),
                Q(postimagen__isnull=True),
                Q(postgaleriaimagen__isnull=True),
                Q(visitaguidadagaleriaimagen__isnull=True)
            )
            kwargs['empty_label'] = 'Sin imagen asociada'

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AgendaAdmin(admin.ModelAdmin):
    inlines = [PostGaleriaImagenInline]




class VisitaGuidadaForm(forms.ModelForm):
    duracion_dias = forms.IntegerField(help_text="Duració en dies")
    duracion_horas = forms.IntegerField(help_text="Duració en hores")

    class Meta:
        model = VisitaGuidada
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        duracion_dias = cleaned_data.get('duracion_dias')
        duracion_horas = cleaned_data.get('duracion_horas')

        if duracion_dias is not None and duracion_horas is not None:
            duracion = f"{duracion_dias} days, {duracion_horas:02d}:00:00"
            cleaned_data['duracion'] = duracion

        return cleaned_data




class VisitaGuidadaGaleriaImagenInline(admin.TabularInline):
    model = VisitaGuidadaGaleriaImagen
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            visita_guidada_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                visita_guidada_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Imagen.objects.filter(
                Q(visitaguidadagaleriaimagen__isnull=True) | Q(visitaguidadagaleriaimagen__visita_guidada__id=visita_guidada_id),
                Q(categoriabannerimagen__isnull=True),
                Q(subblogimagen__isnull=True),
                Q(categoriagaleriaimagen__isnull=True),
                Q(postimagen__isnull=True),
                Q(postgaleriaimagen__isnull=True),
                Q(agendagaleriaimagen__isnull=True)
            )
            kwargs['empty_label'] = 'Sin imagen asociada'

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class VisitaGuidadaAdmin(admin.ModelAdmin):
    form = VisitaGuidadaForm
    inlines = [VisitaGuidadaGaleriaImagenInline]
    filter_horizontal = ('agendas',)
    raw_id_fields = ('mapa','punto_inicio')
    exclude = ['duracion']  # Excluir el campo duracion en el administrador
    

admin.site.register(Agenda, AgendaAdmin)
admin.site.register(VisitaGuidada, VisitaGuidadaAdmin)
