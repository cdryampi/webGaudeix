from django.shortcuts import render
from django.shortcuts import render
from blog.models import Categoria, Post
from header.models import Header, Referencia
from topbar.models import Topbar
from personalizacion.models import Parallax
from redes_sociales.models import RedSocial
from footer.models import Footer
from redes_sociales.utils import obtener_color_mas_repetido
from map.models import MapPoint
from personalizacion.models import PortadaVideo

app_name = 'core'
# Create your views here.

def error_404(request, exception):
    return render(request, 'core/404/error.html', {'message': 'Página no encontrada'})

def home(request):
    
    # Obtén las categorías que deseas mostrar en la página de inicio

    categorias = Categoria.objects.filter(publicado=True)

    # Obtén los últimos posts que deseas mostrar en la página de inicio

    posts = Post.objects.filter(publicado=True).order_by('-fecha')[:3]

    # Renderiza la plantilla de la página de inicio con los datos obtenidos

    # Obtén la instancia de Header

    header = Header.objects.first()

    #Obtén las referencias de header

    referencias = Referencia.objects.filter(header = header)
    topbar = Topbar.objects.filter(publicado =True).last()
    portada = True

    # obtener el último parallax publicado
    parallax = Parallax.objects.filter(publicado=True).last()

    #obtener las redes sociales
    redes_sociales = RedSocial.objects.all()
    
    #obtener color más repetido de las redes sociales
    redes_color = obtener_color_mas_repetido()

    #Seleccionar las categorias especiales.
    categorias_especiales = Categoria.objects.filter(publicado=True, especial=True)

    #Seleccionar los elementos del footer

    footer = Footer.objects.all().first()

    categorias_filtradas = ['platges', "informació", 'jaciments', 'patrimoni']
    # Obtén los puntos del mapa
    map_points = MapPoint.objects.filter(publicado=True, icono__in=categorias_filtradas).values('titulo', 'latitud', 'longitud', 'icono')

    # Agrupa los puntos de mapa por icono
    grouped_points = {}
    for point in map_points:
        icono = point['icono']
        if icono not in grouped_points:
            grouped_points[icono] = []
        grouped_points[icono].append(point)
    print(grouped_points)
    portada_video = PortadaVideo.objects.filter(publicado=True).first()
    videos = []
    if portada_video:
        if portada_video:
            videos_portada = portada_video.videosportada.videos.all()
            for item in videos_portada:
                videos.append(item.archivo.url)
                
    categorias_con_subblog = Categoria.objects.filter(subblog__isnull=False, publicado=True)

    return render(
        request,
        'core/home/home.html',
        {
            'categorias': categorias,
            'posts': posts,
            'header': header,
            'referencias': referencias,
            'topbar': topbar,
            'portada': portada,
            'parallax': parallax,
            'redes_sociales': redes_sociales,
            'color_red_social': redes_color,
            'categorias_especiales': categorias_especiales,
            'footer': footer,
            'videos': videos,
            'map_points': grouped_points,
            'categorias_header': categorias_con_subblog
        }
    )

