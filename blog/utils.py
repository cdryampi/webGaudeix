from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Post
from collections import defaultdict
from django.core.serializers import serialize
from .models import Post
from agenda.models import Agenda

import json






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

    for evento in eventos:
        eventos_por_dia[evento.fecha.day].append(evento)

    # Filtrar las claves que tienen valores inválidos o vacíos
    eventos_por_dia = {k: v for k, v in eventos_por_dia.items() if v}

    # Serializar los objetos Agenda y Post a un formato serializable
    serialized_eventos_por_dia = {}
    for key, value in eventos_por_dia.items():
        serialized_eventos = []
        for evento in value:
            agenda = Agenda.objects.filter(pk=evento.agenda.pk).first()
            if agenda:
                agenda_fields = {
                    'ubicacion': agenda.ubicacion,
                    'descripcion_corta': agenda.descripcion_corta,
                    'tipo_evento': agenda.tipo_evento,
                    # Agrega otros campos de Agenda que necesites
                }
                post = Post.objects.filter(agenda=agenda).first()
                if post:
                    post_fields = {
                        'titulo': post.titulo,
                        'descripcion': post.descripcion,
                        'entradas': post.entradas,
                        'fecha': post.fecha.isoformat() if post.fecha else '',
                        'hora': post.hora.strftime('%H:%M') if post.hora else '',
                        'categoria': post.categoria.titulo if post.categoria else '',
                        'slug': post.categoria.titulo if post.categoria else '',
                        'imagen':agenda.agendagaleriaimagen_set.all().first().imagen.archivo.url if agenda.agendagaleriaimagen_set.all() else '',
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

