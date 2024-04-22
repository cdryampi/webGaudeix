from django.shortcuts import render
from blog.models import Categoria, Post
from agenda.models import VariationAgenda
from header.models import Header, Referencia, HeaderFooter
from topbar.models import Topbar
from personalizacion.models import Parallax
from redes_sociales.models import RedSocial
from footer.models import Footer
from redes_sociales.utils import obtener_color_mas_repetido
from map.models import MapPoint
from multimedia_manager.models import VideosEmbed, Carrusel
from selecciones.models import SeleccionDestacados
from eventos_especiales.models import EventoEspecial
from paginas_estaticas.models import Cookies, PaginaLegal, Diversidad
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django_user_agents.utils import get_user_agent
from gaudeix.settings import TIEMPO_EXPIRACION
from .utils import generate_cache_key
from django.core.cache import caches
from personalizacion.models import Personalizacion
from admin_utils.models import RegistroError
from blog.models import SubBlog
from alerta.models import Alerta
from django.views import View
from django.shortcuts import redirect
from django.http import Http404
from agenda.models import AudioRuta
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from django.http import JsonResponse
from urllib.parse import unquote

import sys




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
        return coleccion_destacados
    return None

def generate_cache_key(request, idioma):
    device_type = 'mobile' if request.user_agent.is_mobile else 'desktop'
    cache_key = f'cache_{idioma}_{device_type}_{request.get_full_path()}'
    return cache_key



def obtener_token_csrf(request):
    token = get_token(request)
    return JsonResponse({'csrf_token': token})
# Vista home cacheada con el tiempo de expiración definido


@csrf_protect
def home(request):

    idioma = request.LANGUAGE_CODE

    cache_key = generate_cache_key(request, idioma)
    cache = caches['default']

    cached_page = cache.get(cache_key)
    if cached_page is not None:
        return cached_page


    alert = None

    personalizacion = Personalizacion.objects.filter().first()

    meta_description = personalizacion.meta_description_portada
    meta_keywords = personalizacion.meta_keywords.all()
    diversidad = Diversidad.objects.filter().first()

    categorias = Categoria.objects.filter(publicado=True)
    ultimos_eventos = get_ultimos_eventos()
    header = Header.objects.first()
    header_footer = HeaderFooter.objects.first()
    referencias = Referencia.objects.filter(header=header)
    
    portada = True
    agenda = Categoria.objects.filter(tipo='agenda').first()
    redes_sociales = RedSocial.objects.all()
    redes_color = obtener_color_mas_repetido()
    categorias_especiales = get_categorias_especiales()
    footer = get_footer()
    map_points = get_map_points()
    coleccion_destacados = get_coleccion_destacados()
    evento = EventoEspecial.objects.filter(publicado=True).first()

    super_destacados = None
    carrusel =  None
    url_iframe_youtube = None

    if personalizacion and personalizacion.superdestacado_set.all():
        super_destacados = personalizacion.superdestacado_set.all()
    if personalizacion and personalizacion.carrusel_portada:
        carrusel = personalizacion.carrusel_portada
    if personalizacion and personalizacion.video_url:
        url_iframe_youtube = personalizacion.video_url
    if personalizacion and personalizacion.alerta:
        alert = personalizacion.alerta
        
    
    # com arribar
    tren = None
    autopista = None
    bus =  None
    aeroport = None
    topbar = None

    subblog = SubBlog.objects.filter(publicado = True).all()

    if personalizacion and personalizacion.video_portada:
        portada_video = personalizacion.video_portada
    else:
        if VideosEmbed.objects.filter(publicado=True).first():
            portada_video = VideosEmbed.objects.filter(publicado=True).first()
        else:
            portada_video = None
    

    if personalizacion and personalizacion.parallax_portada:
        parallax = personalizacion.parallax_portada
    else:
        parallax = Parallax.objects.filter(publicado =True).first()

    
    if personalizacion and personalizacion.topbar:
        topbar = personalizacion.topbar


    if personalizacion and personalizacion.trenpersonalizacion:
        tren = personalizacion.trenpersonalizacion
    
    if personalizacion and personalizacion.autopistapersonalizacion:
        autopista = personalizacion.autopistapersonalizacion

    if personalizacion and personalizacion.buspersonalizacion:
        bus = personalizacion.buspersonalizacion
    
    if personalizacion and personalizacion.aeropuertopersonalizacion:
        aeroport = personalizacion.aeropuertopersonalizacion



    categorias_con_subblog = Categoria.objects.filter(subblog__isnull=False, publicado=True)
    user_agent = get_user_agent(request)
    cookies = Cookies.objects.filter().first()
    cookie_page = PaginaLegal.objects.filter(tipo="cookies").first()
    current_url = request.build_absolute_uri()

    response = render(
        request,
        'core/home/home.html',
        {
            'categorias': categorias,
            'ultimos_eventos': ultimos_eventos,
            'agenda': agenda,
            'header': header,
            'header_footer': header_footer,
            'referencias': referencias,
            'topbar': topbar,
            'portada': portada,
            'redes_sociales': redes_sociales,
            'super_destacados': super_destacados,
            'color_red_social': redes_color,
            'categorias_especiales': categorias_especiales,
            'footer': footer,
            'video_local': portada_video,
            'map_points': map_points,
            'categorias_header': categorias_con_subblog,
            'coleccion_destacados': coleccion_destacados,
            'evento_especial_activo': evento,
            'user_agent': user_agent,
            'parallax':parallax,
            'cookies': cookies,
            'diversidad': diversidad,
            'cookie_page': cookie_page,
            'current_url': current_url,
            'alert': alert,
            'tren': tren,
            'autopista': autopista,
            'bus': bus,
            'aeroport': aeroport,
            'subblogs': subblog,
            'portada_meta_description': meta_description,
            'portada_meta_keywords': meta_keywords,
            'carrusel': carrusel,
            'url_iframe_youtube': url_iframe_youtube
        }
    )
    
    # Guardar la respuesta en la caché con la clave generada
    response['X-Frame-Options'] = 'SAMEORIGIN'  # O 'SAMEORIGIN' si quieres permitir el uso de iframes del mismo dominio
    cache.set(cache_key, response, TIEMPO_EXPIRACION)
    return response


def error_404(request, exception):
    
    categorias = Categoria.objects.filter(publicado=True)
    ultimos_eventos = get_ultimos_eventos()
    header = Header.objects.first()
    header_footer = HeaderFooter.objects.first()
    referencias = Referencia.objects.filter(header=header)
    topbar = Topbar.objects.filter(publicado=True).last()
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
    parallax = Parallax.objects.filter(publicado=True).first()
    user_agent = get_user_agent(request)
    cookies = Cookies.objects.filter().first()
    cookie_page = PaginaLegal.objects.filter(tipo="cookies").first()
    diversidad = Diversidad.objects.filter().first()

    response = render(
        request,
        'core/404/404.html',
        {
            'categorias': categorias,
            'ultimos_eventos': ultimos_eventos,
            'agenda': agenda,
            'header': header,
            'header_footer': header_footer,
            'referencias': referencias,
            'topbar': topbar,
            'redes_sociales': redes_sociales,
            'color_red_social': redes_color,
            'categorias_especiales': categorias_especiales,
            'footer': footer,
            'video_local': portada_video,
            'map_points': map_points,
            'categorias_header': categorias_con_subblog,
            'coleccion_destacados': coleccion_destacados,
            'evento_especial': evento,
            'user_agent': user_agent,
            'parallax':parallax,
            'cookies': cookies,
            'cookie_page': cookie_page,
            'diversidad': diversidad
        }
    )

    return response


def error_500(request):
    
    categorias = Categoria.objects.filter(publicado=True)
    ultimos_eventos = get_ultimos_eventos()
    header = Header.objects.first()
    header_footer = HeaderFooter.objects.first()
    referencias = Referencia.objects.filter(header=header)
    topbar = Topbar.objects.filter(publicado=True).last()
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
    parallax = Parallax.objects.filter(publicado=True).first()
    user_agent = get_user_agent(request)
    cookies = Cookies.objects.filter().first()
    cookie_page = PaginaLegal.objects.filter(tipo="cookies").first()
    diversidad = Diversidad.objects.filter().first()


    exception_type, exception_value, traceback = sys.exc_info()
    error_message = f"{exception_type.__name__}: {str(exception_value)}"
    # Registra el error en la base de datos
    registro_error = RegistroError(
        descripcion=error_message,
        titulo="Error 500 en la aplicación",
    )
    registro_error.save()
    response = render(
        request,
        'core/500/500.html',
        {
            'categorias': categorias,
            'ultimos_eventos': ultimos_eventos,
            'agenda': agenda,
            'header': header,
            'header_footer': header_footer,
            'referencias': referencias,
            'topbar': topbar,
            'redes_sociales': redes_sociales,
            'color_red_social': redes_color,
            'categorias_especiales': categorias_especiales,
            'footer': footer,
            'video_local': portada_video,
            'map_points': map_points,
            'categorias_header': categorias_con_subblog,
            'coleccion_destacados': coleccion_destacados,
            'evento_especial': evento,
            'user_agent': user_agent,
            'parallax':parallax,
            'cookies': cookies,
            'cookie_page': cookie_page,
            'diversidad': diversidad
        }
    )

    return response





# Create your views here.

class RedirectMultimediaFile(View):
    def get(self, request, *args, **kwargs):
        try:
            current_url = request.build_absolute_uri()
            audio_ruta = AudioRuta.objects.get(link_unico=unquote(current_url))
        except AudioRuta.DoesNotExist:
            raise Http404("El enlace no existe")  # Maneja el caso en el que el enlace no se encuentre en la base de datos
        # Realiza el redireccionamiento al enlace único del audio
        return redirect(audio_ruta.audio.archivo.url)