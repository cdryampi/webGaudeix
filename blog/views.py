from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post,SubBlog,Categoria, CategoriaBannerImagen
import json
from header.models import Referencia, Header
from core.mixin.base import BaseContextMixin

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