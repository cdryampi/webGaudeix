from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

class POEditForm(forms.Form):
    content = forms.CharField(
        widget=CKEditor5Widget(
            config_name='idiomas_toolbar'
        ),
    
    label="Contenido del Archivo PO")
