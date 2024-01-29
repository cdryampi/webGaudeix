# Archivo urls.py en la aplicación "core"

from django.urls import include,path
from .views import error_404, home, RedirectMultimediaFile
from .utils import refresh_cache
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Otras URLs de la aplicación "core"
    # ...
    path('', views.home, name='home'),
    path('refresh-cache/', refresh_cache, name='refresh_cache'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots.txt"),
    path('redirect/<str:link_unico>', RedirectMultimediaFile.as_view(),name="redirect_file")
]