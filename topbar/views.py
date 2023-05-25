from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Topbar
# Create your views here.

class TopbarView(TemplateView):
    template_name = 'topbar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topbar'] = Topbar.objects.filter(publicado=True).last()

        return context
