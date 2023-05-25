from blog.models import Categoria
from header.models import Header,Referencia
from topbar.models import Topbar

class BaseContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega aquí las variables de contexto que deseas pasar a la plantilla
        #context['categorias'] = Categoria.objects.filter(publicado=True)
        context['header'] = Header.objects.first()
        context['referencias'] = Referencia.objects.filter(header=context['header'])
        context['topbar'] = Topbar.objects.filter(publicado=True).last()
        return context
