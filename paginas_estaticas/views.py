from .models import PaginaLegal, Contacto, PuntoInformacion, Diversidad
from django.views.generic import TemplateView
from core.mixin.base import BaseContextMixin
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from api.models import Teenvio, MailManager, GmailServer, OutlookServer
from gaudeix.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import EmailMessage
from django.utils.html import escape

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


class PuntInformacioView(BaseContextMixin,TemplateView):
    template_name = 'paginas_estaticas/punt_informacio.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['punt'] = PuntoInformacion.objects.all().first()
        return context



class ContactoView(BaseContextMixin, TemplateView):
    template_name = 'paginas_estaticas/contacto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacto'] = Contacto.objects.all().first()
        return context
    
    def post(self, request):
        # Obtener los datos del formulario

        name = escape(request.POST.get('name'))
        surname = escape(request.POST.get('surname'))
        email = escape(request.POST.get('email'))
        phone = escape(request.POST.get('phone'))
        address = escape(request.POST.get('address'))
        postal_code = escape(request.POST.get('postal_code'))
        city = escape(request.POST.get('city'))
        country = escape(request.POST.get('country'))
        message = escape(request.POST.get('message'))
        privacy_policy = escape(request.POST.get('privacy_policy'))

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
            Hola,

            Has rebut un nou contacte a través del formulari de la web. A continuació, es mostren els detalls:

            Nom: {name}
            Cognoms: {surname}
            Correu electrònic: {email}
            Telèfon: {phone}
            Adreça: {address}
            Codi Postal: {postal_code}
            Ciutat: {city}
            País: {country}
            Missatge: {message}

            Gràcies.

            Atentament,
            El formulari de contacte de la web
        '''


        # Configurar el servidor SMTP y enviar el correo electrónico

        # recuperar la configuración del correo.
        mail_manager = MailManager.objects.filter().first()

        try:
            if privacy_policy:
                mail_manager.mail_server
                if mail_manager.mail_server =='gmail':
                            # Crear el objeto EmailMessage y especificar la codificación
                    gmail_server = GmailServer.objects.filter().first()
                    email = EmailMessage(
                        subject=subject,
                        body=body,
                        from_email=EMAIL_HOST_USER,
                        to=[gmail_server.recipient_email],
                    )
                    email.encoding = 'utf-8'  # Especificar la codificación UTF-8
                    email.send()

                    response_data = {
                    'success': True,
                    'message': 'Missatge enviat correctament.'
                    }

                elif mail_manager.mail_server =='outlook':
                    outlook_server = OutlookServer.objects.filter(mail_server=mail_manager).first()

                    with smtplib.SMTP(outlook_server.smtp_server_url, outlook_server.smtp_server_port) as server:
                        if outlook_server.use_tls:
                            server.starttls()
                        server.login(outlook_server.user, outlook_server.password)
                        server.sendmail(outlook_server.user, outlook_server.recipient_email, body.encode('utf-8').strip())

                        response_data = {
                        'success': True,
                        'message': 'Missatge enviat correctament.'
                        }
                else:
                    response_data = {
                        'success': False,
                        'message': 'servidor no vàlid.'
                    }
                    return JsonResponse(response_data, status=400)
            else:
                response_data = {
                'success': False,
                'message': 'No has aceptado la política de privacidad.'
                }
            
        except Exception as e:
            response_data = {
                'error': str(e)
            }
            print(str(e))
        return JsonResponse(response_data)

class IguadadView(BaseContextMixin,TemplateView):
    template_name = 'paginas_estaticas/igualtat.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diversidad'] = Diversidad.objects.all().first()
        return context
