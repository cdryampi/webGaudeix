# Archivo urls.py en la aplicación "core"

from django.urls import include,path
from .views import EventoEspecialView

app_name = 'eventos_especiales'
urlpatterns = [
    # Otras URLs de la aplicación "core"
    # ...
    path('<slug:slug>', EventoEspecialView.as_view(), name='evento_especial'),
]
