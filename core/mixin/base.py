from blog.models import Categoria
from header.models import Header,Referencia
from topbar.models import Topbar
from footer.models import Footer
from eventos_especiales.models import EventoEspecial

class BaseContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega aquí las variables de contexto que deseas pasar a la plantilla
        #context['categorias'] = Categoria.objects.filter(publicado=True)
        context['header'] = Header.objects.first()
        categorias_con_subblog = Categoria.objects.filter(subblog__isnull=False, publicado=True)
        context['categorias_header'] = categorias_con_subblog
        context['referencias'] = Referencia.objects.filter(header=context['header'])
        context['topbar'] = Topbar.objects.filter(publicado=True).last()
        context['footer'] = Footer.objects.filter().first()
        context['evento_especial'] = EventoEspecial.objects.filter(publicado = True).first()
        return context
