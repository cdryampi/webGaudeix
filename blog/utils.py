from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Post
from collections import defaultdict
from django.core.serializers import serialize
from .models import Post, Noticia
from agenda.models import Agenda, VariationAgenda
from django.http import JsonResponse
from django.http import HttpResponse
from datetime import datetime
import requests
from django.core.serializers.json import DjangoJSONEncoder
import feedparser
import json
from bs4 import BeautifulSoup






class Command(BaseCommand):
    help = 'Assign slugs to existing Post objects'

    def handle(self, *args, **options):
        posts = Post.objects.all()
        for post in posts:
            # Generar el slug basado en el título
            slug = slugify(post.titulo)
            post.slug = slug
            post.save()



def agrupar_eventos_por_dia(eventos):
    
    eventos_por_dia = defaultdict(list)
    #print(eventos[0])
    for evento in eventos:

        agenda = VariationAgenda.objects.filter(pk=evento.pk).first()
        #print(agenda.fecha)
        eventos_por_dia[agenda.fecha.day].append(evento)

    # Filtrar las claves que tienen valores inválidos o vacíos
    eventos_por_dia = {k: v for k, v in eventos_por_dia.items() if v}

    # Serializar los objetos Agenda y Post a un formato serializable
    serialized_eventos_por_dia = {}
    for key, value in eventos_por_dia.items():
        serialized_eventos = []
        for evento in value:
            agenda = VariationAgenda.objects.filter(pk=evento.pk).first()
            if agenda:
                agenda_fields = {
                    'ubicacion': agenda.agenda.ubicacion.titulo,
                    'descripcion_corta': agenda.agenda.descripcion_corta,
                    'tipo_evento': agenda.agenda.tipo_evento,
                    'fecha': agenda.fecha.isoformat() if agenda.fecha else '',
                    'entradas': agenda.agenda.entradas,
                    'hora': agenda.hora.strftime('%H:%M') if agenda.hora else '',
                    'idiomas': [idioma.nombre for idioma in agenda.agenda.idiomas.all()]
                    # Agrega otros campos de Agenda que necesites
                }
                post = Post.objects.filter(agenda=agenda.agenda).first()
                if post:
                    post_fields = {
                        'titulo': post.titulo,
                        'descripcion': post.descripcion,
                        'categoria': post.categoria.titulo if post.categoria else '',
                        'slug': post.slug if post.slug else '',
                        'imagen':agenda.agenda.postgaleriaimagen_set.all().first().imagen.medium_thumbnail.url if agenda.agenda.postgaleriaimagen_set.all() else '',
                        'tags': [tag.nombre for tag in post.tags.all()],
                        # Agrega otros campos de Post que necesites
                    }
                    serialized_evento = {
                        'agenda': agenda_fields,
                        'post': post_fields,
                    }
                    serialized_eventos.append(serialized_evento)

        serialized_eventos_por_dia[key] = serialized_eventos

    return serialized_eventos_por_dia


def sincronizar_noticias():
    # URL del feed RSS
    feed_url = 'https://www.cabrerademar.cat/feeds/noticies'

    # Configurar los encabezados para solicitar XML
    headers = {
        'Accept': 'application/html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    # Realizar la solicitud al feed con los encabezados personalizados
    response = requests.get(feed_url, headers=headers)

    # Obtener y analizar el feed
    feed = feedparser.parse(response.content)


    for entry in feed.entries:
        try:
            # Obtener los datos relevantes de cada entrada del feed
            titulo = entry.title
            descripcion = entry.summary
            fecha = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z').date()
            imagen_url = entry.media_content[0]['url'] if 'media_content' in entry else None

            # Verificar si la noticia ya existe por título
            noticia_existente = Noticia.objects.filter(titulo=titulo).first()
            if noticia_existente:
                # Actualizar las propiedades de la noticia existente
                noticia_existente.contenido = descripcion
                noticia_existente.fecha = fecha
                noticia_existente.imagen_url = imagen_url
                noticia_existente.save()
            else:
                # Crear la noticia si no existe
                noticia = Noticia(
                    titulo=titulo,
                    contenido=descripcion,
                    fecha=fecha,
                    imagen_url=imagen_url,
                    publicado=True,
                    metatitulo=titulo,
                    metadescripcion=descripcion
                )
                noticia.save()

        except Exception as e:
            # Manejar el error en caso de que ocurra durante el proceso de sincronización
            print(f"Error al sincronizar noticia: {str(e)}")


def serialize_restaurante_to_json(restaurantes):
    """
        Función que serealiza una lista de restaurantes.
    """
    restaurantes_list = []
    for restaurante in restaurantes:
        imagen = None
        if restaurante.postimagen.imagen.medium_thumbnail.url:
            imagen = restaurante.postimagen.imagen.medium_thumbnail.url
        else:
            if restaurante.postgaleriaimagen_set.first().imagen.medium_thumbnail.url:
                imagen = restaurante.postgaleriaimagen_set.first().imagen.medium_thumbnail.url
                
        r = {
            # Campos de Restaurante
            "titulo": restaurante.titulo,
            "direccion": restaurante.direccion,
            "telefono": restaurante.telefono,
            "slug":restaurante.slug,
            "sitio_web": restaurante.sitio_web,
            "tipo": restaurante.get_tipo_display(),  # Muestra la representación de string del choice
            # Añadir más campos de Restaurante según sea necesario
            "pet_friendly": restaurante.pet_friendly,
            "opciones_vegetarianas": restaurante.opciones_vegetarianas,
            "wifi": restaurante.wifi,
            "apto_para_celiacos": restaurante.apto_para_celiacos,
            "terraza": restaurante.terraza,
            "menu_infantil": restaurante.menu_infantil,
            "telefono": restaurante.telefono,
            "imagen": imagen,
            # Campos de Post (modelo padre)
            "descripcion": limitar_descripcion_html(restaurante.descripcion, 20),
            # Añadir más campos heredados de Post según sea necesario
        }
        restaurantes_list.append(r)

    return json.dumps(restaurantes_list, cls=DjangoJSONEncoder)



def limitar_descripcion_html(html_content, max_palabras):
    soup = BeautifulSoup(html_content, "html.parser")
    texto_plano = soup.get_text(separator=' ')
    palabras = texto_plano.split()

    if len(palabras) <= max_palabras:
        return html_content

    texto_cortado = ' '.join(palabras[:max_palabras]) + '...'
    soup_cortado = BeautifulSoup(texto_cortado, "html.parser")
    return str(soup_cortado)