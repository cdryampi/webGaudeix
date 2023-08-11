from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from blog.models import Post
from eventos_especiales.models import EventoEspecial
from.models import SeleccionDestacados

class SeleccionForm(forms.ModelForm):
    coleccion = forms.ModelMultipleChoiceField(
        queryset=Post.objects.all(),
        widget=FilteredSelectMultiple('Posts', is_stacked=False),
        required=False,
        label='Posts'
    )

    class Meta:
        model = SeleccionDestacados
        fields = '__all__'

def save_model(self, request, obj, form, change):
    # Guardar el objeto SeleccionDestacados
    obj.save()

    # Obtener los posts seleccionados del formulario
    posts = form.cleaned_data['coleccion']

    # Eliminar todas las relaciones de posts existentes
    obj.posts.clear()

    # Agregar los posts seleccionados a la selección destacada
    obj.posts.set(posts)

    # Guardar la selección destacada con las relaciones actualizadas
    obj.save()

