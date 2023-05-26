from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Parallax

class ParallaxView(TemplateView):
    template_name = 'parallax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parallax'] = Parallax.objects.filter(publicado=True).last()

        return context
