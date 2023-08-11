from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Carrusel, Slide
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