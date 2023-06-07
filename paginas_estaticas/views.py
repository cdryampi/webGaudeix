from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import PaginaLegal
from django.views.generic import TemplateView
from core.mixin.base import BaseContextMixin


class PrivacitatView(BaseContextMixin, TemplateView):
    template_name = 'paginas_estaticas/privacitat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['legal'] = PaginaLegal.objects.get(tipo='privacitat')
        return context

class AvisLegalView(BaseContextMixin, TemplateView):
    template_name = 'paginas_estaticas/avis_legal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['legal'] = PaginaLegal.objects.get(tipo='avis_legal')
        return context

class PoliticaCookiesView(BaseContextMixin, TemplateView):
    template_name = 'paginas_estaticas/politica_cookies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['legal'] = PaginaLegal.objects.get(tipo='cookies')
        return context