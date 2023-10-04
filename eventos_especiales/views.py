from django.shortcuts import render


from django.views.generic import View, DetailView
from core.mixin.base import BaseContextMixin
from django.shortcuts import get_object_or_404
from .models import EventoEspecial
from redes_sociales.models import RedSocial
from personalizacion.models import Parallax
from django.db.models import F
from personalizacion.models import Personalizacion
import random
from django.utils import timezone

# Create your views here.


class EventoEspecialView(BaseContextMixin,DetailView):
    model = EventoEspecial
    template_name = 'eventos_especiales/evento_especial.html'
    context_object_name = 'evento_especial'
    
    def get_object(self, queryset=None):
        # Obtener el objeto de la agenda utilizando el slug en lugar del ID
        slug = self.kwargs.get('slug')
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, slug=slug)
        return obj
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento_especial = self.object
        parallax = evento_especial.parallax
        
        personalizacion = Personalizacion.objects.filter().first()

        # com arribar
        tren = None
        autopista = None
        bus =  None
        aeroport = None

        if personalizacion and personalizacion.trenpersonalizacion:
            tren = personalizacion.trenpersonalizacion
    
        if personalizacion and personalizacion.autopistapersonalizacion:
            autopista = personalizacion.autopistapersonalizacion

        if personalizacion and personalizacion.buspersonalizacion:
            bus = personalizacion.buspersonalizacion
        
        if personalizacion and personalizacion.aeropuertopersonalizacion:
            aeroport = personalizacion.aeropuertopersonalizacion

        redes_sociales= RedSocial.objects.filter().all()
        
        context['tren'] = tren
        context['autopista'] = autopista
        context['bus'] =  bus
        context['aeroport'] = aeroport

        context['redes_sociales'] = redes_sociales
        context['parallax'] = parallax
        context['now'] = timezone.now()

        return context