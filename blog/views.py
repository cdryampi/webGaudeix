from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post,SubBlog,Categoria, CategoriaBannerImagen
from agenda.models import Agenda
from django.http import JsonResponse
from django.views.generic import View
from header.models import Referencia, Header
from core.mixin.base import BaseContextMixin
from personalizacion.models import Parallax
from redes_sociales.models import RedSocial

class ListarPostsView(ListView):
    model = Post
    template_name = 'blog/listar_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Implementa aquí tu lógica personalizada para filtrar o manipular la queryset
        queryset = super().get_queryset().filter(publicado=True)
        return queryset

class DetallePostView(DetailView):
    model = Post
    template_name = 'blog/detalle_post.html'
    context_object_name = 'post'

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

class CategoriaDetailView(BaseContextMixin, DetailView):
    model = Categoria
    template_name = 'blog/detalle_categoria.html'
    context_object_name = 'categoria'
    pk_url_kwarg = 'categoria_id'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el objeto de la categoría actual
        categoria = context['categoria']

        # Verificar si el tipo de categoría es "agenda"
        if categoria.tipo == 'agenda':
            # Obtener la lista de agendas relacionadas
            agendas = Agenda.objects.filter(publicado=True).all()
            parallax = Parallax.objects.filter(publicado= True).first()
            redes_sociales= RedSocial.objects.filter().all()
            context['redes_sociales'] = redes_sociales
            context['parallax'] = parallax
            context['agendas'] = agendas

        return context


class FiltrarAgendaAPI(View):
    def get(self, request):
        # Obtener el parámetro de filtrado desde la URL
        tipo_evento = request.GET.get('tipo_evento')

        # Filtrar las agendas según el tipo de evento
        agendas = Agenda.objects.filter(publicado=True, tipo_evento=tipo_evento)

        # Serializar los resultados del filtro como JSON
        data = []
        for agenda in agendas:
            data.append({
                'id': agenda.id,
                'titulo': agenda.titulo,
                'ubicacion': agenda.ubicacion,
                'descripcion_corta': agenda.descripcion_corta,
                # Agrega más campos según tus necesidades
            })

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