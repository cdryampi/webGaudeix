# Archivo urls.py en la aplicación "core"

from django.urls import include,path
from .views import error_404, home
from .utils import refresh_cache
from . import views

urlpatterns = [
    # Otras URLs de la aplicación "core"
    # ...
    path('', views.home, name='home'),
    path('refresh-cache/', refresh_cache, name='refresh_cache')
]


