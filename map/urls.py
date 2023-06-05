from django.urls import path
from .views import CoordenadasAyuntamientoAPI

urlpatterns = [
        path('api/coordenadas-ayuntamiento/', CoordenadasAyuntamientoAPI.as_view(), name='coordenadas_ayuntamiento_api'),

]
