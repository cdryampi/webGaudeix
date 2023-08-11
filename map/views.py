from django.http import JsonResponse
from .models import MapPoint
from agenda.models import Agenda, Ruta


from django.db.models import F
import random

from django.views.generic import View, DetailView
from core.mixin.base import BaseContextMixin
from django.shortcuts import get_object_or_404
from django.db.models import F, ExpressionWrapper



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
        puntos = MapPoint.objects.filter(publicado=True, icono__in=categorias_filtradas)

        # Calcular los valores de las imágenes y almacenarlos en una lista de diccionarios
        puntos_data = []

        for punto in puntos:
            small_thumbnail_url = ''  # Puedes usar un valor predeterminado aquí
            large_thumbnail_url = ''
            try:
                if punto.postimagen:
                    imagen = punto.postimagen.imagen
                if imagen:
                    small_thumbnail_url = imagen.small_thumbnail.url
                    large_thumbnail_url = imagen.large_thumbnail.url
                else:
                    # Si no hay imagen, proporciona un valor predeterminado o deja en blanco
                    small_thumbnail_url = ''  # Puedes usar un valor predeterminado aquí
                    large_thumbnail_url = ''

            except Exception as e:
                pass



            punto_data = {
                'titulo': punto.titulo,
                'latitud': punto.latitud,
                'longitud': punto.longitud,
                'icono': punto.icono,
                'small_thumbnail_url': small_thumbnail_url,
                'large_thumbnail_url': large_thumbnail_url,
                'descripcion': punto.descripcion,
                'slug': punto.slug,
            }

            puntos_data.append(punto_data)

        return JsonResponse(puntos_data, safe=False)

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
        # Obtener todos los puntos de mapa publicados, excluyendo el objeto actual
        llocs = MapPoint.objects.filter(publicado=True).exclude(pk=current_object.pk)

        # Obtener una muestra aleatoria de 4 elementos de la lista de puntos de mapa
        random_llocs = random.sample(list(llocs), 4)

        # Obtener las rutas vinculadas a este mapa
        rutes = Ruta.objects.filter(mapas_itinerario=current_object).all()
        context['llocs'] = random_llocs
        context['rutes'] = rutes
        return context

