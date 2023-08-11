from django.views.generic import View, DetailView,ListView
from core.mixin.base import BaseContextMixin
from django.shortcuts import get_object_or_404
from .models import Subvencion, SubvencionDescripcion
# Create your views here.


class SubvencionsListView(BaseContextMixin,DetailView):
    model = SubvencionDescripcion
    template_name = 'subvenciones/subvencion_list.html'
    context_object_name = 'SubvencionDescripcion'
    
    
    
    def get_object(self, queryset=None):
        # Obtener el objeto de la agenda utilizando el slug en lugar del ID
        obj = SubvencionDescripcion.objects.first()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.get_object()
        subvenciones= Subvencion.objects.filter(publicado=True).all()
        context['subvenciones'] = subvenciones

        return context

class SubvencionListView(BaseContextMixin,DetailView):
    model = Subvencion
    template_name = 'subvenciones/subvencion_detail.html'
    context_object_name = 'subvencio'
    
    
    
    def get_object(self, queryset=None):
        # Obtener el objeto de la agenda utilizando el slug en lugar del ID
        slug = self.kwargs.get('slug')
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, slug=slug)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.get_object()


        return context