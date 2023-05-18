# Archivo urls.py en la aplicación "core"

from django.urls import include,path
from .views import error_404


urlpatterns = [
    # Otras URLs de la aplicación "core"
    # ...
    path('404/', error_404, name='error_404'),
]
