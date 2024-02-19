from django.template.loader import render_to_string
from blog.models import SubBlog, Categoria
from gaudeix.settings import DOMAIN_URL
from header.models import Header
from personalizacion.models import Personalizacion
from redes_sociales.models import RedSocial
from footer.models import Footer
from django.utils import translation
from header.models import Referencia

def gen_html_evento_especial(newsletter, evento_especial):
    """
        función que genera las queryset para la plantilla del correo.
    """
    header = Header.objects.filter().first()
    referencias = Referencia.objects.filter(header=header)
    personalizacion = Personalizacion.objects.filter().first()
    redes_sociales = RedSocial.objects.filter().all()
    categorias_especiales = Categoria.objects.filter(especial = True).all()
    footer = Footer.objects.filter().first()

    html_content = render_to_string(
        'newsletter/event_email.html',
        {
            'evento_especial': evento_especial,
            'newsletter': newsletter,
            'url_domain': DOMAIN_URL,
            'header': header,
            'personalizacion': personalizacion,
            'redes_sociales': redes_sociales,
            'categorias_especiales': categorias_especiales,
            'referencias': referencias,
            'footer': footer
        }
    )

    html_content_encoded = html_content.encode('utf-8')
    return html_content_encoded