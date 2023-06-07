"""
URL configuration for gaudeix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from multimedia_manager.urls import urlpatterns as url_media
#from multimedia_manager.filters import ImagenAutocomplete
from django.urls import re_path
from django_select2 import urls as select2_urls

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include(('core.urls', 'core'), namespace='core')),
    path('blog/',include('blog.urls')),
    path('agenda/',include('agenda.urls')),
    path('map/',include('map.urls')),
    path('personalizacion/',include('personalizacion.urls')),
    path('paginas_estaticas/', include('paginas_estaticas.urls'))
    # re_path(
    #     r'^imagen-autocomplete/$',
    #     ImagenAutocomplete.as_view(),
    #     name='imagen-autocomplete',
    # ),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
