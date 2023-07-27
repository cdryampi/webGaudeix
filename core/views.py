from django.shortcuts import render
from blog.models import Categoria, Post
from agenda.models import VariationAgenda
from header.models import Header, Referencia
from topbar.models import Topbar
from personalizacion.models import Parallax
from redes_sociales.models import RedSocial
from footer.models import Footer
from redes_sociales.utils import obtener_color_mas_repetido
from map.models import MapPoint
from personalizacion.models import VideosEmbed, SeleccionDestacados
from eventos_especiales.models import EventoEspecial
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.cache import cache_page
from gaudeix.settings import TIEMPO_EXPIRACION

app_name = 'core'

# Función para obtener las últimas agendas del portal
def get_ultimos_eventos():
    now = timezone.now()
    return VariationAgenda.objects.filter(
        Q(agenda__publicado=True) &
        Q(fecha__gte=now.date()) &
        (Q(fecha=now.date(), hora__gte=now.time()) | Q(fecha__gt=now.date()))
    ).order_by('fecha', 'hora')[:4]

# Función para obtener las categorías especiales
def get_categorias_especiales():
    return Categoria.objects.filter(publicado=True, especial=True)

# Función para obtener los elementos del footer
def get_footer():
    return Footer.objects.all().first()

# Función para obtener los puntos del mapa
def get_map_points():
    categorias_filtradas = ['platges', "informació", 'jaciments', 'patrimoni']
    return MapPoint.objects.filter(publicado=True, icono__in=categorias_filtradas).order_by('icono').all()

# Función para obtener los Post seleccionados explícitamente
def get_coleccion_destacados():
    coleccion_destacados = SeleccionDestacados.objects.filter(publicado=True).first()
    if coleccion_destacados:
        return coleccion_destacados.coleccion.all()
    return None

# Vista home cacheada con el tiempo de expiración definido
@cache_page(TIEMPO_EXPIRACION)
def home(request):
    categorias = Categoria.objects.filter(publicado=True)
    ultimos_eventos = get_ultimos_eventos()
    header = Header.objects.first()
    referencias = Referencia.objects.filter(header=header)
    topbar = Topbar.objects.filter(publicado=True).last()
    portada = True
    agenda = Categoria.objects.filter(tipo='agenda').first()
    redes_sociales = RedSocial.objects.all()
    redes_color = obtener_color_mas_repetido()
    categorias_especiales = get_categorias_especiales()
    footer = get_footer()
    map_points = get_map_points()
    coleccion_destacados = get_coleccion_destacados()
    evento = EventoEspecial.objects.filter(publicado=True).first()
    portada_video = VideosEmbed.objects.filter(publicado=True).first()
    categorias_con_subblog = Categoria.objects.filter(subblog__isnull=False, publicado=True)

    return render(
        request,
        'core/home/home.html',
        {
            'categorias': categorias,
            'ultimos_eventos': ultimos_eventos,
            'agenda': agenda,
            'header': header,
            'referencias': referencias,
            'topbar': topbar,
            'portada': portada,
            'redes_sociales': redes_sociales,
            'color_red_social': redes_color,
            'categorias_especiales': categorias_especiales,
            'footer': footer,
            'video_local': portada_video,
            'map_points': map_points,
            'categorias_header': categorias_con_subblog,
            'coleccion_destacados': coleccion_destacados,
            'evento_especial': evento,
        }
    )

def error_404(request, exception):
    return render(request, 'core/404/error.html', {'message': 'Página no encontrada'}, status=404)