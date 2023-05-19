# En blog/forms.py

from django import forms
from .models import Categoria, Imagen
from dal import autocomplete
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'subblog': autocomplete.ModelSelect2(url='subblog-autocomplete'),
        }
