from django import forms
from ckeditor.widgets import CKEditorWidget

class POEditForm(forms.Form):
    content = forms.CharField(
        widget=CKEditorWidget(
            config_name='idiomas_toolbar'
        ),
    
    label="Contenido del Archivo PO")
