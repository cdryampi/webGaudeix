from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Q
from multimedia_manager.models import Imagen, Fichero
from .models import Agenda, VisitaGuiada
from map.models import MapPoint
from django.forms import DurationField
from blog.models import PostImagen, PostGaleriaImagen, PostFichero
from django import forms
from django.utils.translation import gettext_lazy as _
from datetime import timedelta


class PostGaleriaImagenInline(admin.TabularInline):
    model = PostGaleriaImagen
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            agenda_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                agenda_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Imagen.objects.filter(
                Q(postgaleriaimagen__isnull=True) | Q(postgaleriaimagen__post__id=agenda_id),
                Q(categoriabannerimagen__isnull=True),
                Q(subblogimagen__isnull=True),
                Q(categoriagaleriaimagen__isnull=True),
                Q(postimagen__isnull=True),
            )
            kwargs['empty_label'] = 'Sin imagen asociada'

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AgendaAdmin(admin.ModelAdmin):
    inlines = [PostGaleriaImagenInline]




class VisitaGuidadaForm(forms.ModelForm):
    duracion_dias = forms.IntegerField(help_text="Duració en dies")
    duracion_horas = forms.IntegerField(help_text="Duració en hores")

    class Meta:
        model = VisitaGuiada
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.duracion:
            duracion = self.instance.duracion
            if isinstance(duracion, str):
                duracion = timedelta(days=0, hours=0)
            duracion_dias = duracion.days
            duracion_horas = duracion.seconds // 3600
            self.initial['duracion_dias'] = duracion_dias
            self.initial['duracion_horas'] = duracion_horas

    def clean(self):
        cleaned_data = super().clean()
        duracion_dias = cleaned_data.get('duracion_dias')
        duracion_horas = cleaned_data.get('duracion_horas')

        if duracion_dias is not None and duracion_horas is not None:
            duracion = timedelta(days=duracion_dias, hours=duracion_horas)
            cleaned_data['duracion'] = duracion
        else:
            # Obtener el valor anterior de duracion si existe
            duracion_anterior = self.instance.duracion
            if isinstance(duracion_anterior, str):
                # Convertir la duracion_anterior a timedelta si es una cadena de texto
                duracion_anterior = timedelta(days=0, hours=0)
            cleaned_data['duracion'] = duracion_anterior

        return cleaned_data








class VisitaGuidadaGaleriaImagenInline(admin.TabularInline):
    model = PostGaleriaImagen
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            visita_guiada_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                visita_guiada_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Imagen.objects.filter(
                Q(postgaleriaimagen__isnull=True) | Q(postgaleriaimagen__post__id=visita_guiada_id),
                Q(categoriabannerimagen__isnull=True),
                Q(subblogimagen__isnull=True),
                Q(categoriagaleriaimagen__isnull=True),
                Q(postimagen__isnull=True),
            )
            kwargs['empty_label'] = 'Sin imagen asociada'

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PostFicheroImagenInline(admin.TabularInline):
    model = PostFichero
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'fichero':
            agenda_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                agenda_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Fichero.objects.filter(
                Q(postfichero__isnull=True) | Q(postfichero__post__id=agenda_id),
            )
            kwargs['empty_label'] = 'Sin fichero asociado'

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class VisitaGuidadaAdmin(admin.ModelAdmin):
    form = VisitaGuidadaForm
    inlines = [VisitaGuidadaGaleriaImagenInline, PostFicheroImagenInline]
    filter_horizontal = ('agendas',)
    raw_id_fields = ('mapa','punto_inicio')
    exclude = ['duracion']  # Excluir el campo duracion en el administrador
    

admin.site.register(Agenda, AgendaAdmin)
admin.site.register(VisitaGuiada, VisitaGuidadaAdmin)
