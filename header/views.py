from django.views.generic import TemplateView
from .models import Header

class HeaderView(TemplateView):
    template_name = 'header.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['header'] = Header.objects.first()
        except Exception:
            # Manejar el error aquí
            context['header'] = None

        return context
