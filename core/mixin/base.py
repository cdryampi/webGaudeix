from blog.models import Categoria
from header.models import Header,Referencia, HeaderFooter
from topbar.models import Topbar
from footer.models import Footer
from eventos_especiales.models import EventoEspecial
from redes_sociales.models import RedSocial
from agenda.models import VariationAgenda
from django.utils import timezone
from django.db.models import Q
from paginas_estaticas.models import Cookies, PaginaLegal, Diversidad

class BaseContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega aquí las variables de contexto que deseas pasar a la plantilla
        #context['categorias'] = Categoria.objects.filter(publicado=True)

    
        # ultimos eventos del portal
        now = timezone.now()
        variation_agendas = VariationAgenda.objects.filter(
            Q(agenda__publicado=True) &
            Q(fecha__gte=now.date()) &
            (Q(fecha=now.date(), hora__gte=now.time()) | Q(fecha__gt=now.date()))
        ).order_by('fecha', 'hora')[:4]

        context['diversidad'] = Diversidad.objects.filter().first()
        context['header_footer'] = HeaderFooter.objects.first()
        context['header'] = Header.objects.first()
        categorias_con_subblog = Categoria.objects.filter(subblog__isnull=False, publicado=True)
        context['categorias_header'] = categorias_con_subblog
        context['referencias'] = Referencia.objects.filter(header=context['header'])
        context['topbar'] = Topbar.objects.filter(publicado=True).last()
        context['footer'] = Footer.objects.filter().first()
        context['evento_especial_activo'] = EventoEspecial.objects.filter(publicado = True).first()
        context['redes_sociales'] = RedSocial.objects.all()
        context['ultimos_eventos'] = variation_agendas
        context['agenda'] = Categoria.objects.filter(publicado=True, tipo='agenda').first()
        context['cookies'] = Cookies.objects.filter().first()
        context['cookie_page'] = PaginaLegal.objects.filter(tipo="cookies").first()
        
        # Obten la URL canónica y agrega al contexto
        canonical_url = self.get_canonical_url()
        context['canonical_url'] = canonical_url

        return context
    def get_canonical_url(self):
        # Lógica para obtener la URL canónica, por ejemplo, desde la URL de la vista actual
        # Si tu lógica es más compleja, puedes modificar esta función en consecuencia
        return self.request.build_absolute_uri()