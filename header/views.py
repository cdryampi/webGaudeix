from django.views.generic import TemplateView
from .models import Header
from blog.models import Categoria

class HeaderView(TemplateView):
    template_name = 'header.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['header'] = Header.objects.first()
            # Filtrar las categorías que tienen un subblog asignado
            categorias_con_subblog = Categoria.objects.filter(subblog__isnull=False, publicado=True)
            context['categorias_header'] = categorias_con_subblog
        except Exception:
            # Manejar el error aquí
            context['header'] = None
            context['categorias_header'] = None

        return context