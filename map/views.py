from django.views import View
from django.http import JsonResponse
from .models import MapPoint

class CoordenadasAyuntamientoAPI(View):
    def get(self, request):
        ayuntamiento_coordenadas = MapPoint.objects.filter(icono="town-hall").first()
        if ayuntamiento_coordenadas:
            data = {
                'latitud': ayuntamiento_coordenadas.latitud,
                'longitud': ayuntamiento_coordenadas.longitud
            }
        else:
            data = {
                'latitud': 41.123456,
                'longitud': 2.987654
            }
        return JsonResponse(data)
