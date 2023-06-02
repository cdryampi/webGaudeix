from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime
from django.db.models import Q
from django.template.loader import render_to_string

import calendar

from .models import Agenda

def generate_pdf(request):
    # Obtener el año y mes actual
    anio_actual = datetime.now().year
    mes_actual = datetime.now().month

    # Filtrar los eventos por año, mes y eventos futuros
    agendas = Agenda.objects.filter(fecha__year=anio_actual, fecha__month=mes_actual, fecha__gte=datetime.now().date()).order_by('fecha')

    # Crear el contexto con los eventos agrupados por fecha
    agendas_por_fecha = {}
    for agenda in agendas:
        fecha = agenda.fecha.strftime("%d/%m/%Y")
        if fecha not in agendas_por_fecha:
            agendas_por_fecha[fecha] = []
        agendas_por_fecha[fecha].append(agenda)

    # Renderizar la plantilla a HTML con el contexto
    html = render_to_string('agenda/agenda_pdf.html', {'agendas_por_fecha': agendas_por_fecha})

    # Crear el objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="agenda.pdf"'

    # Generar el PDF utilizando xhtml2pdf
    pisa.CreatePDF(html, dest=response)

    return response