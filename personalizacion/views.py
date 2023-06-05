from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Parallax, PortadaVideo
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
        portada_video = PortadaVideo.objects.all().first()
        videos = []

        if portada_video:
            videos_portada = portada_video.videosportada_set.all().order_by('orden')
            videos = [vp.video for vp in videos_portada]

        context['videos'] = videos
        return context


class PortadaVideoAPIView(View):
    def get(self, request, *args, **kwargs):
        portada_video = PortadaVideo.objects.filter(publicado=True).first()
        videos = []
        if portada_video:
            videos_portada = portada_video.videosportada.videos.all()
            for item in videos_portada:
                videos.append(item.archivo.url)

        if portada_video:
            data = {
                'videos': videos
                # Agrega más campos si es necesario
            }
        else:
            data = {}

        return JsonResponse(data)