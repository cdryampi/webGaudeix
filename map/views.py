from django.views import View
from django.http import JsonResponse
from .models import MapPoint
from django.views.generic import View, DetailView
from core.mixin.base import BaseContextMixin
from django.shortcuts import get_object_or_404

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
        categorias_filtradas = ['platges', "informació", 'jaciments', 'patrimoni']
        puntos = MapPoint.objects.filter(publicado=True, icono__in=categorias_filtradas).values('titulo', 'latitud', 'longitud', 'icono')
        return JsonResponse(list(puntos), safe=False)
    

class MapaView(BaseContextMixin, DetailView):
    model = MapPoint
    template_name = 'map/mapa-post.html'
    context_object_name = 'map'

    def get_object(self, queryset=None):
        # Obtener el objeto de la agenda utilizando el slug en lugar del ID
        
        slug = self.kwargs.get('slug')
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, slug=slug)
        return obj
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.get_object()
        return context
