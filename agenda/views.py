from django.shortcuts import render
from django.views.generic import ListView, DetailView,TemplateView
from .models import Agenda
from core.mixin.base import BaseContextMixin

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from django.db.models import Q
from datetime import datetime,timedelta


# Create your views here.
class AgendaListView(BaseContextMixin,ListView):
    model = Agenda
    template_name = 'agenda/agenda.html'
    context_object_name = 'agendas'

class PDFView(View):
    def get(self, request):
        # Obtener el año y mes actual
        anio_actual = datetime.now().year
        mes_actual = datetime.now().month
        

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
        agendas = Agenda.objects.filter(
            Q(fecha__gte=datetime.now().date(), fecha__lte=datetime.now().date() + timedelta(days=30), publicado=True)
        ).order_by('fecha')

        for _ in range(2):  # Iterar dos veces para cubrir los próximos dos meses
            if mes_actual == 11:
                mes_actual += 1
                if mes_actual > 12:
                    mes_actual = 1
                    anio_actual += 1
            #meses_a_pintar.append(meses_traduccion[mes_actual])

            # Crear un diccionario para agrupar las agendas por fecha
            agendas_por_mes[meses_traduccion[mes_actual]] = {}

            for agenda in agendas:
                fecha = agenda.fecha.strftime("%d")
                day_of_the_week = agenda.fecha.isocalendar().weekday-1
                agenda_mes = str(str(fecha)+" "+str(dias_letras[day_of_the_week]))
                

                if  mes_actual == agenda.fecha.month:
                    
                    if agenda_mes not in agendas_por_mes[meses_traduccion[mes_actual]]:
                        agendas_por_mes[meses_traduccion[mes_actual]][agenda_mes] = []
                        agendas_por_mes[meses_traduccion[mes_actual]][agenda_mes].append(agenda)
                    else:
                        agendas_por_mes[meses_traduccion[mes_actual]][agenda_mes].append(agenda)
            

            if mes_actual > 12:
                mes_actual = 1
                anio_actual += 1
            else:
                mes_actual +=1
        # Obtener la plantilla HTML
        template = get_template('agenda/agenda_pdf.html')
        # Crear el diccionario de contexto
        print(agendas_por_mes)
        context = {
            'anio_actual': anio_actual,
            'agendas': agendas_por_mes
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