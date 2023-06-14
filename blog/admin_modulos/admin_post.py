from django.contrib import admin
from ..models import PostImagen,PostGaleriaImagen,Post
from multimedia_manager.models import Imagen
from django.db.models import Q
from ..models import Tag
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=FilteredSelectMultiple("Etiquetas", is_stacked=False),
        required=False,
    )

    class Meta:
        model = Post
        fields = "__all__"



class PostImagenInline(admin.TabularInline):
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
                    Q(postimagen__isnull=True) | Q(postimagen__post__id=post_id)
                )
            kwargs['empty_label'] = 'Sense imatge associada'
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PostGaleriaImagenInline(admin.TabularInline):
    model = PostGaleriaImagen
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            # Obtener el ID del post actual
            post_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                post_id = request.resolver_match.kwargs['object_id']
            
            # Filtrar las imágenes disponibles para seleccionar
                kwargs['queryset'] = Imagen.objects.filter(
                    Q(categoriabannerimagen__isnull=True),
                    Q(subblogimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True),
                    Q(postimagen__isnull=True),
                    Q(postgaleriaimagen__isnull=True)
                    | Q(postgaleriaimagen__post__id=post_id),
                )
            kwargs['empty_label'] = 'Sin imagen asociada'
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('titulo', 'fecha', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('titulo', 'descripcion')
    inlines = [PostImagenInline, PostGaleriaImagenInline]
    fields = ['titulo', 'descripcion', 'fecha', 'hora', 'categoria']
    
    def get_queryset(self, request):
        # Obtener el queryset original
        queryset = super().get_queryset(request)
        
        # Filtrar los objetos de tipo Agenda
        queryset = queryset.exclude(agenda__isnull=False).exclude(visitaguidada__isnull=False)
        
        return queryset