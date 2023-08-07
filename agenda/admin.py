from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Q
from multimedia_manager.models import Imagen, Fichero
from .models import Agenda, VisitaGuiada, Ruta, VariationAgenda
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
                Q(eventoespecialgaleriaimagen__isnull=True),
            )
            kwargs['empty_label'] = 'Sin imagen asociada'

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class VariationAgendaInline(admin.TabularInline):
    model = VariationAgenda
    extra = 0

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
                Q(eventofichero__isnull=True)
            )
            kwargs['empty_label'] = 'Sin fichero asociado'

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PostImagenInlineRuta(admin.TabularInline):
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
                    Q(categoriabannerimagen__isnull=True),
                    Q(subblogimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True),
                    Q(postgaleriaimagen__isnull=True),
                    Q(eventoespecialgaleriaimagen__isnull=True),
                    Q(postimagen__isnull=True) | Q(postimagen__post__id=post_id)
                )
            kwargs['empty_label'] = 'Sense imatge associada'
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)





class AgendaAdmin(admin.ModelAdmin):
    inlines = [PostGaleriaImagenInline, VariationAgendaInline, PostFicheroImagenInline]
    autocomplete_fields = ['ubicacion']





class VisitaGuidadaForm(forms.ModelForm):
    duracion_dias = forms.IntegerField(help_text="Duració en dies", required=False)
    duracion_horas = forms.IntegerField(help_text="Duració en hores", required=False)

    class Meta:
        model = VisitaGuiada
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.duracion:
            duracion = self.instance.duracion
            duracion_dias = duracion.days
            duracion_horas = duracion.seconds // 3600
            self.initial['duracion_dias'] = duracion_dias
            self.initial['duracion_horas'] = duracion_horas

    def clean(self):
        cleaned_data = super().clean()
        duracion_dias = cleaned_data.get('duracion_dias')
        duracion_horas = cleaned_data.get('duracion_horas')

        duracion = timedelta()

        if duracion_dias:
            duracion += timedelta(days=duracion_dias)

        if duracion_horas:
            duracion += timedelta(hours=duracion_horas)

        cleaned_data['duracion'] = duracion

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        duracion_dias = self.cleaned_data.get('duracion_dias')
        duracion_horas = self.cleaned_data.get('duracion_horas')

        if duracion_dias is not None and duracion_horas is not None:
            duracion = timedelta(days=duracion_dias, hours=duracion_horas)
            instance.duracion = duracion

        if commit:
            instance.save()

        return instance




class VisitaGuidadaAdmin(admin.ModelAdmin):
    form = VisitaGuidadaForm
    inlines = [PostImagenInlineRuta, PostGaleriaImagenInline, PostFicheroImagenInline]
    filter_horizontal = ('agendas',)
    exclude = ['duracion']  # Excluir el campo duracion en el administrador
    







class RutaAdmin(admin.ModelAdmin):
    form = VisitaGuidadaForm
    inlines = [PostGaleriaImagenInline, PostFicheroImagenInline, PostImagenInlineRuta]
    exclude = ['duracion']  # Excluir el campo duracion en el administrador


admin.site.register(Ruta, RutaAdmin)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(VisitaGuiada, VisitaGuidadaAdmin)
