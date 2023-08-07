from django.views.generic import ListView, DetailView
from .models import Post,SubBlog,Categoria, CategoriaBannerImagen, Noticia
from agenda.models import Agenda, VisitaGuiada, Ruta, VariationAgenda
from django.http import JsonResponse
from django.views.generic import View
from core.mixin.base import BaseContextMixin
from personalizacion.models import Parallax, Carrusel
from redes_sociales.models import RedSocial
from .utils import agrupar_eventos_por_dia
from django.db.models import Q
import json
from django.shortcuts import get_object_or_404
from django.utils import timezone
from eventos_especiales.models import EventoEspecial
class ListarPostsView(ListView):
    model = Post
    template_name = 'blog/listar_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Implementa aquí tu lógica personalizada para filtrar o manipular la queryset
        queryset = super().get_queryset().filter(publicado=True)
        return queryset

class DetallePostView(BaseContextMixin,DetailView):
    model = Post
    template_name = 'blog/detalle_post.html'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object


        return context


class ListarSubBlogView(ListView):
    model = SubBlog
    template_name = 'blog/listar_subblog.html'
    context_object_name = 'blogs'
    def get_queryset(self):
        # Implementa aquí tu lógica personalizada para filtrar o manipular la queryset
        queryset = super().get_queryset().filter(publicado=True)
        return queryset
    

    

class DetalleSubBlogView(BaseContextMixin, DetailView):
    model = SubBlog
    template_name = 'blog/detalle_subblog.html'
    context_object_name = 'subblog'
    pk_url_kwarg = 'subblog_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subblog_actual = self.object
        context['categorias'] = Categoria.objects.filter(subblog=subblog_actual)
        
        return context

class CategoriaDetailView(BaseContextMixin, DetailView):
    model = Categoria
    template_name = 'blog/detalle_categoria.html'
    context_object_name = 'categoria'
    pk_url_kwarg = 'categoria_id'

    def get_object(self, queryset=None):
        # Obtener el objeto de la agenda utilizando el slug en lugar del ID
        slug = self.kwargs.get('slug')
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, slug=slug)
        return obj


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el objeto de la categoría actual
        categoria = context['categoria']
        categorias_hermanas = Categoria.objects.filter(publicado= True).exclude(id=categoria.id)
        context['categorias'] = categorias_hermanas
        now = timezone.now()
        # Verificar si el tipo de categoría es "agenda"
        if categoria.tipo == 'agenda':
            # Obtener la lista de agendas relacionadas
            agendas = Agenda.objects.filter(publicado=True).all()
            parallax = Parallax.objects.filter(publicado= True).first()
            redes_sociales= RedSocial.objects.filter().all()
            categorias = Categoria.objects.filter(publicado=True)
            context['redes_sociales'] = redes_sociales
            context['parallax'] = parallax
            context['agendas'] = agendas
            context['joves'] = VariationAgenda.objects.filter(agenda__publicado= True, agenda__tipo_evento='joves',fecha__gt=now).first()
            context['categorias'] = categorias

        elif categoria.tipo == 'visitas_guiadas':
            visitas_guiadas = VisitaGuiada.objects.filter(publicado=True, categoria = categoria).all()
            context['visitas_guiadas'] = visitas_guiadas

        elif categoria.tipo == 'noticies':
            noticias = Noticia.objects.filter(publicado=True, categoria=categoria).all()
            context['noticias'] = noticias

        elif categoria.tipo == 'senderisme':
            rutes  = Ruta.objects.filter(publicado=True).all()
            context['rutes'] = rutes

        elif categoria.tipo == 'normal':
            posts = Post.objects.filter(publicado = True, categoria = categoria)
            context['posts'] = posts

        elif categoria.tipo == 'lloc':
            posts = Post.objects.filter(publicado = True, categoria = categoria)
            context['posts'] = posts
        elif categoria.tipo == 'festes_i_tradicions':
            festes = EventoEspecial.objects.filter().all()
            posts = Post.objects.filter(publicado = True, categoria = categoria)
            context['posts'] = posts
            context['festes'] = festes
            
        return context





class FiltrarAgendaView(View):
    def post(self, request, *args, **kwargs):
        # Obtener el parámetro de filtrado desde la solicitud POST
        tipo_evento = request.POST.get('tipo_evento')
        year_str = request.POST.get('year')
        month_str = request.POST.get('month')

        # Convertir los valores de año y mes a enteros
        year = int(year_str)
        month = int(month_str)

        # Filtrar las agendas según el tipo de evento
        agendas = VariationAgenda.objects.filter(agenda__publicado=True)

        agendas = agendas.filter(
            Q(fecha__year=year, fecha__month=month + 1) |
            Q(fecha__isnull=True)
        )

        if tipo_evento:
            agendas = agendas.filter(agenda__tipo_evento=tipo_evento)

        # Serializar los resultados del filtro

        eventos_agrupados = agrupar_eventos_por_dia(agendas)

        serialized_agendas = json.dumps(eventos_agrupados)

        # Crear el diccionario de respuesta JSON
        data = {
            'agendas': serialized_agendas,
        }

        # Devolver la respuesta JSON con los resultados del filtro
        return JsonResponse(data, safe=False)


class ListarCategoria(ListView):
    model = Categoria
    template_name = 'blog/listar_categorias.html'
    context_object_name = 'categorias'
    
    def get_queryset(self):
        # Implementa aquí tu lógica personalizada para filtrar o manipular la queryset
        queryset = super().get_queryset().filter(publicado=True)
        #print(queryset.first())
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorias = context['categorias']

        for categoria in categorias:
            try:
                banner_imagen = CategoriaBannerImagen.objects.get(categoria=categoria)
                categoria.banner_imagen = banner_imagen.imagen.archivo
                #print(categoria.banner_imagen.url)
            except CategoriaBannerImagen.DoesNotExist:
                categoria.banner_imagen = None
        # Imprimir el contexto como JSON

        return context
    


class SeleccionDestacadosCategoria(ListView):
    model = Categoria
    template_name = 'blog/listar_categoria_destacados.html'
    context_object_name = 'categorias'


# vistas previas del admin
class DetalleNoticiaView(BaseContextMixin, DetailView):
    model = Noticia
    template_name = 'blog/noticia.html'
    context_object_name = 'noticia'