from django.shortcuts import render
from .models import CompraDescubre
from django.views.generic import View, DetailView
from core.mixin.base import BaseContextMixin
from django.shortcuts import get_object_or_404
from django.utils import timezone
from redes_sociales.models import RedSocial
# Create your views here.



class CompaDescubreView(BaseContextMixin,DetailView):
    model = CompraDescubre
    template_name = 'compra_y_descubre/compra_y_descubre.html'
    context_object_name = 'compra_y_descubre'
    
    def get_object(self, queryset=None):
        # Obtener el objeto de la agenda utilizando el slug en lugar del ID
        slug = self.kwargs.get('slug')
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, slug=slug)
        return obj
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento_especial = self.object
        redes_sociales= RedSocial.objects.filter().all()
        context['redes_sociales'] = redes_sociales
        context['now'] = timezone.now()
        return context