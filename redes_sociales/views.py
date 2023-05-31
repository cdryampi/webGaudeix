from django.views.generic import TemplateView
from .models import RedSocial

class RedSocialListView(TemplateView):
    template_name = 'redes_sociales/redes_sociales.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['redes_sociales'] = RedSocial.objects.all()
        return context