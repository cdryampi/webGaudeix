# from dal import autocomplete

# from django import forms
# from .models import Imagen
# from django.utils.html import format_html
# from django.utils.safestring import mark_safe
# import os

# class ImagenForm(forms.ModelForm):
#     class Meta:
#         model = Imagen
#         fields = '__all__'
#         widgets = {
#             'titulo': autocomplete.ListSelect2(url='imagen-autocomplete'),
#             'archivo': forms.FileInput(attrs={'class': 'image-file-input'}),
#         }
#     def clean(self):
#         cleaned_data = super().clean()
        
#         # Obtener el valor del campo "titulo" y "archivo"
#         titulo = cleaned_data.get('titulo')
#         archivo = cleaned_data.get('archivo')
        
#         # Realizar las modificaciones necesarias
#         if not archivo and titulo:
#             # Obtener la imagen correspondiente al título del filtro
#             imagen = Imagen.objects.filter(titulo=titulo).first()
            
#             # Asignar la imagen al campo "archivo"
#             if imagen:
#                 if self.cleaned_data['archivo']:
#                     archivo_name = self.cleaned_data['archivo'].name
#                 else:
#                     archivo_name = ''

#                 cleaned_data['archivo'] = imagen.archivo

        
#         return cleaned_data
    
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         if self.cleaned_data['archivo']:
#             instance.titulo = os.path.splitext(self.cleaned_data['archivo'].name)[0]
#         if commit:
#             instance.save()
#         return instance