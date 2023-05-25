from django.shortcuts import render
from django.shortcuts import render
from blog.models import Categoria, Post
from header.models import Header, Referencia
from topbar.models import Topbar


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

    print("HI")

    return render(request, 'core/home/home.html', {'categorias': categorias, 'posts': posts, 'header': header, 'referencias':referencias, 'topbar':topbar})

