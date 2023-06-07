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
    

class MapPointAPI(View):
    def get(self, request):
        puntos = MapPoint.objects.all().values('titulo', 'latitud', 'longitud', 'icono')
        return JsonResponse(list(puntos), safe=False)
