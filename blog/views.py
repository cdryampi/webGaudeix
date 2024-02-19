from django.views.generic import ListView, DetailView
from .models import Post,SubBlog,Categoria, CategoriaBannerImagen, Noticia, SubCategoria
from agenda.models import Agenda, VisitaGuiada, Ruta, VariationAgenda, Alojamiento, Restaurante
from django.http import JsonResponse
from django.views.generic import View
from core.mixin.base import BaseContextMixin
from redes_sociales.models import RedSocial
from .utils import agrupar_eventos_por_dia, serialize_restaurante_to_json
from django.db.models import Q
import json
from django.shortcuts import get_object_or_404
from django.utils import timezone
from eventos_especiales.models import EventoEspecial
from personalizacion.models import Personalizacion
from multimedia_manager.models import Parallax
from django.core.serializers import serialize
from django.http import JsonResponse

class ListarPostsView(ListView):
    """
    Vista basada en clase para listar todos los posts.
    Utiliza una plantilla 'listar_posts.html' para mostrar la lista de posts.
    """
    model = Post  # Modelo que se utilizará para obtener los posts
    template_name = 'blog/post/listar_posts.html'  # Plantilla HTML para la página
    context_object_name = 'posts'  # Nombre con el que se pasará la lista de posts a la plantilla

    def get_queryset(self):
        """
        Devuelve la queryset de posts filtrada para mostrar solo los publicados.
        """
        queryset = super().get_queryset().filter(publicado=True)
        return queryset

class DetallePostView(BaseContextMixin, DetailView):
    """
    Vista basada en clase para mostrar los detalles de un post específico.
    Utiliza una plantilla 'detalle_post.html' para mostrar los detalles.
    """
    model = Post  # Modelo que se utilizará para obtener el post
    template_name = 'blog/post/detalle_post.html'  # Plantilla HTML para la página
    context_object_name = 'post'  # Nombre con el que se pasará el objeto post a la plantilla

    def get_context_data(self, **kwargs):
        """
        Agrega datos adicionales al contexto de la plantilla.
        """
        context = super().get_context_data(**kwargs)
        # Puedes agregar aquí cualquier dato adicional que quieras pasar a la plantilla
        return context


class ListarSubBlogView(ListView):
    """
    Vista basada en clase para listar los subblogs publicados.
    Utiliza una plantilla 'listar_subblog.html' para mostrar la lista de subblogs.
    """
    model = SubBlog  # Modelo que se utilizará para obtener los subblogs
    template_name = 'blog/subblog/listar_subblog.html'  # Plantilla HTML para la página
    context_object_name = 'blogs'  # Nombre con el que se pasará la lista de subblogs a la plantilla

    def get_queryset(self):
        """
        Devuelve la queryset de subblogs filtrada para mostrar solo los publicados.
        """
        queryset = super().get_queryset().filter(publicado=True)
        return queryset


class DetalleSubBlogView(BaseContextMixin, DetailView):
    """
    Vista basada en clase para mostrar los detalles de un subblog específico.
    Utiliza una plantilla 'detalle_subblog.html' para mostrar los detalles.
    """
    model = SubBlog  # Modelo que se utilizará para obtener el subblog
    template_name = 'blog/subblog/detalle_subblog.html'  # Plantilla HTML para la página
    context_object_name = 'subblog'  # Nombre con el que se pasará el objeto subblog a la plantilla
    pk_url_kwarg = 'subblog_id'  # Nombre del argumento de URL para identificar el subblog

    def get_context_data(self, **kwargs):
        """
        Agrega datos adicionales al contexto de la plantilla.
        """
        context = super().get_context_data(**kwargs)
        subblog_actual = self.object
        # Filtrar y agregar las categorías relacionadas con el subblog actual al contexto
        context['categorias'] = Categoria.objects.filter(subblog=subblog_actual)
        return context


class CategoriaDetailView(BaseContextMixin, DetailView):
    """
    Vista basada en clase para mostrar los detalles de una categoría específica.
    Utiliza una plantilla 'detalle_categoria.html' para mostrar los detalles.
    """
    model = Categoria # Modelo que se utilizará para obtener la categoría
    template_name = 'blog/categorias/detalle_categoria.html' # Plantilla HTML para la página
    context_object_name = 'categoria' # Nombre con el que se pasará el objeto categoría a la plantilla
    pk_url_kwarg = 'categoria_id' # Nombre del argumento de URL para identificar la categoría

    def get_object(self, queryset=None):
        # Obtener el objeto de la agenda utilizando el slug en lugar del ID
        slug = self.kwargs.get('slug')
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, slug=slug)
        return obj


    def get_context_data(self, **kwargs):
        """
        Agrega datos adicionales al contexto de la plantilla.
        """
        context = super().get_context_data(**kwargs)
        # Obtener el objeto de la categoría actual
        categoria = context['categoria']
        categorias_hermanas = Categoria.objects.filter(publicado= True).exclude(id=categoria.id)
        context['categorias'] = categorias_hermanas
        now = timezone.now()
        # Verificar si el tipo de categoría es "agenda"
        if categoria.tipo == 'agenda':
            # Si la categoría es de tipo 'agenda', obtener la lista de agendas relacionadas
            agendas = Agenda.objects.filter(publicado=True).all()
            parallax = Personalizacion.objects.filter().first()

            if parallax is not None:
                if parallax.parallax_agenda:
                    parallax = parallax.parallax_agenda.parallax_agenda
                else:
                    parallax = None
            else:
                parallax = Parallax.objects.filter().first()
            
            redes_sociales= RedSocial.objects.filter().all()
            categorias = Categoria.objects.filter(publicado=True)
            context['redes_sociales'] = redes_sociales
            context['parallax'] = parallax
            context['agendas'] = agendas
            context['joves'] = VariationAgenda.objects.filter(agenda__publicado= True, agenda__tipo_evento='joves',fecha__gt=now).first()
            context['categorias'] = categorias

        elif categoria.tipo == 'visitas_guiadas':
            # Si la categoría es de tipo 'visitas_guiadas', obtener las visitas guiadas relacionadas
            visitas_guiadas = VisitaGuiada.objects.filter(publicado=True, categoria = categoria).all()
            context['visitas_guiadas'] = visitas_guiadas

        elif categoria.tipo == 'noticies':
            # Si la categoría es de tipo 'noticias', obtener las noticias relacionadas
            noticias = Noticia.objects.filter(publicado=True, categoria=categoria).all()
            context['noticias'] = noticias

        elif categoria.tipo == 'senderisme':
            # Si la categoría es de tipo 'senderisme', obtener las rutas relacionadas
            rutes  = Ruta.objects.filter(publicado=True).all()
            context['rutes'] = rutes

        elif categoria.tipo == 'allotjament':
            alojamientos = Alojamiento.objects.filter(publicado=True, categoria=categoria).all()
            context['alojamientos'] = alojamientos
            posts = Post.objects.filter(publicado = True, categoria = categoria).exclude(alojamiento__isnull=False)
            context['posts'] = posts

        elif categoria.tipo == 'restaurant':
            restaurantes = Restaurante.objects.filter(publicado=True, categoria=categoria).all()
            context['restaurantes'] = restaurantes
            posts = Post.objects.filter(publicado = True, categoria = categoria).exclude(restaurante__isnull=False)
            context['posts'] = posts
            
        elif categoria.tipo == 'normal':
            # Si la categoría es de tipo 'normal', obtener los posts relacionados
            posts = Post.objects.filter(publicado = True, categoria = categoria)
            context['posts'] = posts

        elif categoria.tipo == 'lloc':
            # Si la categoría es de tipo 'lloc', obtener los posts relacionados
            posts = Post.objects.filter(publicado = True, categoria = categoria)
            context['posts'] = posts
            
        elif categoria.tipo == 'festes_i_tradicions':
            # Si la categoría es de tipo 'festes_i_tradicions', obtener las festividades relacionadas
            festes = EventoEspecial.objects.filter(categoria = self.get_object()).all()
            posts = Post.objects.filter(publicado = True, categoria = categoria)
            context['posts'] = posts
            context['festes'] = festes
            
        return context

class FiltrarAgendaView(View):
    """
    Vista basada en clase para filtrar las agendas de eventos.
    """
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
    """
    Vista basada en clase para listar las categorías en una página.
    Utiliza una plantilla 'listar_categorias.html' para mostrar la lista de categorías.
    """
    model = Categoria  # Modelo que se utilizará para obtener las categorías
    template_name = 'blog/categorias/listar_categorias.html'  # Plantilla HTML para la página
    context_object_name = 'categorias'  # Nombre con el que se pasará la lista de categorías a la plantilla
    
    def get_queryset(self):
        """
        Devuelve la queryset de categorías filtrada para mostrar solo las publicadas.
        """
        queryset = super().get_queryset().filter(publicado=True)
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Agrega datos adicionales al contexto de la plantilla.
        """
        context = super().get_context_data(**kwargs)
        categorias = context['categorias']

        for categoria in categorias:
            try:
                banner_imagen = CategoriaBannerImagen.objects.get(categoria=categoria)
                categoria.banner_imagen = banner_imagen.imagen.archivo
            except CategoriaBannerImagen.DoesNotExist:
                categoria.banner_imagen = None

        # Puedes imprimir el contexto como JSON aquí si necesitas depurar

        return context

    

class DetalleNoticiaView(BaseContextMixin, DetailView):
    """
    Vista basada en clase para mostrar los detalles de una noticia específica.
    Utiliza una plantilla 'noticias/noticia.html' para mostrar los detalles.
    """
    model = Noticia  # Modelo que se utilizará para obtener la noticia
    template_name = 'blog/noticias/noticia.html'  # Plantilla HTML para la página
    context_object_name = 'noticia'  # Nombre con el que se pasará el objeto noticia a la plantilla
    
class ListarNoticiaView(BaseContextMixin, ListView):
    """
    Vista basada en clase para listar las noticias.
    Utiliza una plantilla 'noticies.html' para mostrar la lista de noticias.
    """
    model = Noticia  # Modelo que se utilizará para obtener los subblogs
    template_name = 'blog/noticias/noticies.html'  # Plantilla HTML para la página
    context_object_name = 'noticias'  # Nombre con el que se pasará la lista de subblogs a la plantilla
    queryset = Noticia.objects.filter(publicado=True).order_by("fecha")


    def get_context_data(self, **kwargs):
        """
        Agrega datos adicionales al contexto de la plantilla.
        """
        context = super().get_context_data(**kwargs)

        return context
    




class SubCategoriaDetailView(BaseContextMixin, DetailView):
    """
    Vista basada en clase para mostrar los detalles de una categoría específica.
    Utiliza una plantilla 'detalle_categoria.html' para mostrar los detalles.
    """
    model = SubCategoria # Modelo que se utilizará para obtener la categoría
    template_name = 'blog/subcategorias/detalle_subcategoria.html' # Plantilla HTML para la página
    context_object_name = 'subcategoria' # Nombre con el que se pasará el objeto categoría a la plantilla
    pk_url_kwarg = 'subcategoria_id' # Nombre del argumento de URL para identificar la categoría

    def get_object(self, queryset=None):
        # Obtener el objeto de la agenda utilizando el slug en lugar del ID
        slug = self.kwargs.get('slug')
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, slug=slug)
        return obj


    def get_context_data(self, **kwargs):
        """
        Agrega datos adicionales al contexto de la plantilla.
        """
        context = super().get_context_data(**kwargs)
        # Obtener el objeto de la categoría actual
        subcategoria = context['subcategoria']
        subcategorias_hermanas = SubCategoria.objects.filter(publicado= True).exclude(id=subcategoria.id)
        context['categorias'] = subcategorias_hermanas
        now = timezone.now()
        #Verificar si el tipo de categoría es "agenda"
        if subcategoria.tipo == 'agenda':
            # Si la categoría es de tipo 'agenda', obtener la lista de agendas relacionadas
            agendas = Agenda.objects.filter(publicado=True).all()
            parallax = Personalizacion.objects.filter().first()

            if parallax is not None:
                if parallax.parallax_agenda:
                    parallax = parallax.parallax_agenda.parallax_agenda
                else:
                    parallax = None
            else:
                parallax = Parallax.objects.filter().first()
            
            redes_sociales= RedSocial.objects.filter().all()
            categorias = SubCategoria.objects.filter(publicado=True)
            context['redes_sociales'] = redes_sociales
            context['parallax'] = parallax
            context['agendas'] = agendas
            context['joves'] = VariationAgenda.objects.filter(agenda__publicado= True, agenda__tipo_evento='joves',fecha__gt=now).first()
            context['categorias'] = categorias

        elif subcategoria.tipo == 'visitas_guiadas':
            # Si la categoría es de tipo 'visitas_guiadas', obtener las visitas guiadas relacionadas
            visitas_guiadas = VisitaGuiada.objects.filter(publicado=True, subcategoria = subcategoria).all()
            context['visitas_guiadas'] = visitas_guiadas

        elif subcategoria.tipo == 'noticies':
            # Si la categoría es de tipo 'noticias', obtener las noticias relacionadas
            noticias = Noticia.objects.filter(publicado=True, subcategoria=subcategoria).all()
            context['noticias'] = noticias

        elif subcategoria.tipo == 'senderisme':
            # Si la categoría es de tipo 'senderisme', obtener las rutas relacionadas
            rutes  = Ruta.objects.filter(publicado=True, subcategoria= subcategoria).all()
            context['rutes'] = rutes

        elif subcategoria.tipo == 'normal':
            # Si la categoría es de tipo 'normal', obtener los posts relacionados
            posts = Post.objects.filter(publicado = True, subcategoria = subcategoria)
            context['posts'] = posts

        elif subcategoria.tipo == 'lloc':
            # Si la categoría es de tipo 'lloc', obtener los posts relacionados
            posts = Post.objects.filter(publicado = True, subcategoria = subcategoria)
            context['posts'] = posts
        elif subcategoria.tipo == 'festes_i_tradicions':
            # Si la categoría es de tipo 'festes_i_tradicions', obtener las festividades relacionadas
            festes = EventoEspecial.objects.filter(categoria = self.get_object().categoria).all()
            posts = Post.objects.filter(publicado = True, subcategoria = subcategoria)
            context['posts'] = posts
            context['festes'] = festes
            
        return context
    

class RestaurantAPI(View):
    """
    Vista basada en clase para filtrar los restaurantes.
    """
    def post(self, request, *args, **kwargs):
        # Obtener el parámetro de filtrado desde la solicitud POST
        tipo_restaurante = request.POST.get('tipo_restaurante')

        # Filtrar las agendas según el tipo de evento

        restaurantes = Restaurante.objects.filter(publicado=True)


        if tipo_restaurante in ['bar','restaurant','masia','guingueta']:
            restaurantes = restaurantes.filter(tipo=tipo_restaurante)


        # Serializar los resultados del filtro
        serialized_restaurantes = serialize_restaurante_to_json(restaurantes)

        # Devolver la respuesta JSON con los resultados del filtro
        return JsonResponse(serialized_restaurantes, safe=False, content_type="application/json")