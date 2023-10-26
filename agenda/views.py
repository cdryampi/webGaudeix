from .models import Agenda, VisitaGuiada, Ruta, VariationAgenda
from blog.models import Post
from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from django.db.models import Q, Max
from datetime import datetime,timedelta
from core.mixin.base import BaseContextMixin
from django.utils import timezone
import itertools
import emoji
import re
from blog.models import Categoria
from personalizacion.models import Personalizacion
from gaudeix.settings import DOMAIN_URL

# Create your views here.
class VisitaGuiadaView(BaseContextMixin, DetailView):
    model = VisitaGuiada
    template_name = 'agenda/visita_guiada.html'
    context_object_name = 'visites'



    def get_object(self, queryset=None):
        # Obtener el objeto de la agenda utilizando el slug en lugar del ID
        
        slug = self.kwargs.get('slug')
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, slug=slug)
        return obj
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.get_object()

       
        visita_guiadas = VisitaGuiada.objects.filter(publicado=True).exclude(pk=current_object.pk)
        categorias = Categoria.objects.filter(publicado= True).all()
        #print("Agendas Relacionadas:", agendas_relacionadas)

        context['coleccion_destacados'] = visita_guiadas
        context['categorias'] = categorias
        context['agendas_relacionadas'] = current_object.agendas.all()
        return context

class RutaView(BaseContextMixin, DetailView):
    model = Ruta
    template_name = 'agenda/ruta.html'
    context_object_name = 'ruta'

    def get_object(self, queryset=None):
        # Obtener el objeto de la agenda utilizando el slug en lugar del ID
        
        slug = self.kwargs.get('slug')
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, slug=slug)
        return obj
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.get_object()
        # Obtener los puntos de itinerario ordenados alfabéticamente
        puntos_itinerario = current_object.mapas_itinerario.all().order_by('titulo')
        rutes = Ruta.objects.filter(publicado = True).exclude(pk = current_object.pk)
        now = timezone.now()
        ultimos_post = Agenda.objects.filter(publicado = True)[:4]
        
        context['rutes'] = rutes
        context['puntos_itinerario'] = puntos_itinerario
        context['now'] = now
        context['posts'] = ultimos_post

        return context


class AgendaDetailView(BaseContextMixin, DetailView):
    model = Agenda
    template_name = 'agenda/agenda.html'
    context_object_name = 'local_agenda'

    def get_object(self, queryset=None):
        # Obtener el objeto de la agenda utilizando el slug en lugar del ID
        slug = self.kwargs.get('slug')
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, slug=slug)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el objeto actual
        current_object = self.get_object()
        now = timezone.now()
        show_ticket_section = False
        for variation in current_object.variationagenda_set.all():
            if now.date() <= variation.fecha:
                show_ticket_section = True
                break
        # Filtrar los eventos futuros utilizando objetos Q y obtener el primer objeto VariationAgenda de cada Agenda
        variation_agendas = VariationAgenda.objects.filter(
            Q(agenda__publicado=True)
        ).order_by('-fecha', '-hora')

        same_type_event = []
        future_events_near = []
        future_events_distant = []
        past_events = []

        for event in variation_agendas:
            if event.agenda.tipo_evento == current_object.tipo_evento:   
                same_type_event.append(event)
            elif event.fecha >= now.date():
                # Calcular la diferencia en días desde la fecha actual
                days_difference = (event.fecha - now.date()).days
                if days_difference <= 7:
                    future_events_near.append(event)  # Futuros cercanos
                else:
                    future_events_distant.append(event)  # Futuros lejanos
            else:
                past_events.append(event)

        # Concatenar los eventos agrupados en una lista plana en el orden deseado
        all_events = same_type_event + future_events_near + future_events_distant + past_events

        # coger el parallax de personalización

        parallax = Personalizacion.objects.filter().first()

        if parallax is not None:
            if parallax.parallax_agenda:
                parallax = parallax.parallax_agenda.parallax_agenda
            else:
                parallax = None
        else:
            parallax = None
        
        context['parallax'] = parallax
        context['coleccion_destacados'] = all_events[:20]
        context['entrades'] = show_ticket_section
        return context




class PDFView(View):
    def get(self, request):

        fecha_actual = datetime.now()
        fecha_siguiente = fecha_actual + timedelta(days=30)

        emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticonos
                           u"\U0001F300-\U0001F5FF"  # símbolos y pictogramas
                           u"\U0001F680-\U0001F6FF"  # transporte y símbolos de mapas
                           u"\U0001F1E0-\U0001F1FF"  # banderas de países
                           u"\U00002600-\U000027BF"  # otros símbolos
                           u"\U0001F900-\U0001F9FF"  # símbolos suplementarios
                           u"\U0001F1F2-\U0001F1F4"  # banderas suplementarias
                           u"\U0001F1E6-\U0001F1FF"  # banderas suplementarias
                           u"\U0001F600-\U0001F64F"  # emoticonos
                           u"\U0001F680-\U0001F6FF"  # transporte y símbolos de mapas
                           u"\U00002600-\U000027BF"  # otros símbolos
                           u"\U0001F300-\U0001F5FF"  # símbolos y pictogramas
                           u"\U0001F1E0-\U0001F1FF"  # banderas de países
                           u"\U00002702-\U000027B0"  # otros símbolos
                           u"\U000024C2-\U0001F251"  # otros símbolos
                           "]+", flags=re.UNICODE)

        
        # Diccionario de traducción de meses
        meses_traduccion = {
            1: 'Gener',
            2: 'Febrer',
            3: 'Març',
            4: 'Abril',
            5: 'Maig',
            6: 'Juny',
            7: 'Juliol',
            8: 'Agost',
            9: 'Setembre',
            10: 'Octubre',
            11: 'Novembre',
            12: 'Desembre',
        }
        dias_letras = {
            0: 'Dilluns',
            1: 'Dimarts',
            2: 'Dimecres',
            3: 'Dijous',
            4: 'Divendres',
            5: 'Dissabte',
            6: 'Diumenge',
        }
        agendas_por_mes = {}

        # Obtener todas las agendas ordenadas por fecha
        agendas = VariationAgenda.objects.filter(
            Q(fecha__gte=datetime.now().date(), fecha__lte=datetime.now().date() + timedelta(days=30), agenda__publicado=True)
        ).order_by('fecha')
        mes_actual = fecha_actual.month
        mes_posterior = fecha_siguiente.month
        # Crear un diccionario para agrupar las agendas por fecha
        agendas_por_mes[meses_traduccion[mes_actual]] = {}
        agendas_por_mes[meses_traduccion[mes_posterior]] = {}

        for agenda in agendas:
            fecha = agenda.fecha.strftime("%d")
            day_of_the_week = agenda.fecha.isocalendar().weekday-1
            agenda_mes = str(str(fecha) + " " + str(dias_letras[day_of_the_week]))
            try:
                if mes_actual == agenda.fecha.month:
                    if agenda_mes not in agendas_por_mes[meses_traduccion[mes_actual]]:
                        agendas_por_mes[meses_traduccion[mes_actual]][agenda_mes] = []
                        agendas_por_mes[meses_traduccion[mes_actual]][agenda_mes].append(agenda)
                    else:
                        agendas_por_mes[meses_traduccion[mes_actual]][agenda_mes].append(agenda)
                if mes_actual+1 == agenda.fecha.month:
                    agendas_por_mes[meses_traduccion[agenda.fecha.month]][agenda_mes] = []
                    agendas_por_mes[meses_traduccion[agenda.fecha.month]][agenda_mes].append(agenda)
            except Exception as e:
                pass


        # Convertir los emojis y los iconos a texto plano
        for mes, agendas_mes in agendas_por_mes.items():
            for dia, agendas_dia in agendas_mes.items():
                for agenda in agendas_dia:
                    agenda.agenda.titulo = emoji_pattern.sub('', agenda.agenda.titulo)
                    agenda.agenda.descripcion_corta = emoji_pattern.sub('', agenda.agenda.descripcion_corta)
                    # También puedes aplicar emoji.demojize a otros campos de Agenda que contengan emojis

        # Obtener la plantilla HTML
        template = get_template('agenda/agenda_pdf.html')

        # contexto para el logo de Cabrera de Mar
        logo_imagen = DOMAIN_URL+'/static/core/img/logos/logo-cabrera-main.png'

        # Crear el diccionario de contexto
        context = {
            'anio_actual': fecha_actual.year,
            'agendas': agendas_por_mes,
            'logo_imagen': logo_imagen
        }
        rendered_template = template.render(context)

        # Crear el objeto PDF
        pdf_file = BytesIO()
        pisa.CreatePDF(rendered_template, dest=pdf_file)

        # Obtener el contenido del PDF
        pdf_content = pdf_file.getvalue()

        # Cerrar el objeto BytesIO
        pdf_file.close()

        # Crear la respuesta HTTP con el contenido del PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="agenda.pdf"'
        response.write(pdf_content)

        return response