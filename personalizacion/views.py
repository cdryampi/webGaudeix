from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Parallax, VideosEmbed
from django.http import JsonResponse
from django.views import View


class ParallaxView(TemplateView):
    template_name = 'parallax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parallax'] = Parallax.objects.filter(publicado=True).last()

        return context

class PortadaVideoView(TemplateView):
    template_name = 'portada-video.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portada_video = VideosEmbed.objects.all().first()

        context['videos'] = portada_video

        return context
