from django.contrib import admin
from .models import Agenda, GaleriaAgenda
from multimedia_manager.models import Imagen
from django.db.models import Q
from blog.models import Tag
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms




class AgendaForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=FilteredSelectMultiple("Etiquetas", is_stacked=False),
        required=False,
    )

    class Meta:
        model = Agenda
        fields = "__all__"
    


class GaleriaAgendaInline(admin.TabularInline):
    model = GaleriaAgenda
    extra = 1
    readonly_fields = ['imagen_preview']

    def imagen_preview(self, instance):
        if instance.imagen:
            return instance.imagen.imagen_thumbnail()
        return '(Cap imatge associada)'

    imagen_preview.short_description = 'Imatge associada'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            agenda_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                agenda_id = request.resolver_match.kwargs['object_id']
            kwargs['queryset'] = Imagen.objects.filter(
                Q(galeriaagenda__isnull=True) | Q(galeriaagenda__agenda_id=agenda_id),
                categoriabannerimagen__isnull=True,
                categoriagaleriaimagen__isnull=True,
                postimagen__isnull=True,
                postgaleriaimagen__isnull = True,
                subblogimagen__isnull=True
            )
            kwargs['empty_label'] = 'Sense imatge associada'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




class AgendaAdmin(admin.ModelAdmin):
    form = AgendaForm
    inlines = [GaleriaAgendaInline]


admin.site.register(Agenda, AgendaAdmin)
