from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Carrusel, Slide, SeleccionDestacados
from blog.models import Post

class CarruselForm(forms.ModelForm):
    slides = forms.ModelMultipleChoiceField(
        queryset=Slide.objects.all(),
        widget=FilteredSelectMultiple('Slides', is_stacked=False),
        required=False,
        label='Slides'
    )

    class Meta:
        model = Carrusel
        fields = '__all__'

    def save_model(self, request, obj, form, change):
        # Guardar el objeto Carrusel
        obj.save()

        # Obtener los sliders seleccionados del formulario
        sliders = form.cleaned_data['slides']

        # Agregar los sliders al carrusel
        obj.slides.set(sliders)

        # Guardar el carrusel con las relaciones actualizadas
        obj.save()


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

