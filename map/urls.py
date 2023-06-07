from django.urls import path
from .views import CoordenadasAyuntamientoAPI,MapPointAPI

urlpatterns = [
        path('api/coordenadas-ayuntamiento/', CoordenadasAyuntamientoAPI.as_view(), name='coordenadas_ayuntamiento_api'),
        path('api/map-points/', MapPointAPI.as_view(), name='map_points_api'),
]
