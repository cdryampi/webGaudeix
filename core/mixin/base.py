from blog.models import Categoria
from header.models import Header,Referencia


class BaseContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega aquí las variables de contexto que deseas pasar a la plantilla
        #context['categorias'] = Categoria.objects.filter(publicado=True)
        context['header'] = Header.objects.first()
        context['referencias'] = Referencia.objects.filter(header=context['header'])
        return context
