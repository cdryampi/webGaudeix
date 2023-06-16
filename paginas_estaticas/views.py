from .models import PaginaLegal, Contacto
from django.views.generic import TemplateView
from core.mixin.base import BaseContextMixin
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from api.models import Teenvio
from gaudeix.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import EmailMessage

import requests

class PrivacitatView(BaseContextMixin, TemplateView):
    template_name = 'paginas_estaticas/privacitat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['legal'] = PaginaLegal.objects.get(tipo='privacitat')
        return context

class AvisLegalView(BaseContextMixin, TemplateView):
    template_name = 'paginas_estaticas/avis_legal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['legal'] = PaginaLegal.objects.get(tipo='avis_legal')
        return context

class PoliticaCookiesView(BaseContextMixin, TemplateView):
    template_name = 'paginas_estaticas/politica_cookies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['legal'] = PaginaLegal.objects.get(tipo='cookies')
        return context

class ContactoView(BaseContextMixin, TemplateView):
    template_name = 'paginas_estaticas/contacto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacto'] = Contacto.objects.all().first()
        return context
    
    def post(self, request):
        # Obtener los datos del formulario
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code')
        city = request.POST.get('city')
        country = request.POST.get('country')
        message = request.POST.get('message')
        privacy_policy = request.POST.get('privacy_policy')

        # Validar el correo electrónico
        try:
            validate_email(email)
        except ValidationError:
            response_data = {
                'error': 'Dirección de correo electrónico inválida'
            }
            return JsonResponse(response_data, status=400)
        
        # Construir el cuerpo del correo electrónico
        subject = 'Nou contacte'
        body = f'''
        Nombre: {name}
        Apellidos: {surname}
        Email: {email}
        Teléfono: {phone}
        Dirección: {address}
        Código Postal: {postal_code}
        Ciudad: {city}
        País: {country}
        Mensaje: {message}
        '''

        # Crear el objeto EmailMessage y especificar la codificación
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=EMAIL_HOST_USER,
            to=['ysanchez@cabrerademar.cat'],
        )
        email.encoding = 'utf-8'  # Especificar la codificación UTF-8

        # Configurar el servidor SMTP y enviar el correo electrónico
        try:
            email.send()

            response_data = {
                'success': True,
                'message': 'Correo electrónico enviado exitosamente'
            }
        except Exception as e:
            response_data = {
                'error': str(e)
            }
            print(str(e))
        return JsonResponse(response_data)