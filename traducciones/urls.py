from django.urls import path
from .utils import edit_view  # Asegúrate de que la importación refleje la ubicación real de tu vista

# Asume que urlpatterns ya está definido, solo añades tu ruta personalizada
urlpatterns = [
    path('traducciones/translation/<int:object_id>/change/', edit_view, name='translation-edit'),
]
