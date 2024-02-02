from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import requests
from .models import Teenvio, Subscriptor
from django.utils.html import escape

import json

class TeenvioView(View):
    template_name = 'api/teenvio_form.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        #print(request.POST.get('email'))
        # Obtener el correo electrónico del formulario
        email = escape(request.POST.get('email'))
        #print(email)
        try:
            validate_email(email)
        except ValidationError:
            response_data = {
                'error': 'Dirección de correo electrónico inválida'
            }
            return JsonResponse(response_data, status=400)
        
        # Verificar si ya existe un subscriptor con el mismo correo electrónico
        try:
            subscriptor = Subscriptor.objects.get(email=email)
        except Subscriptor.DoesNotExist:
            # Si no existe, crear un nuevo subscriptor
            email_parts = email.split('@')
            name = email_parts[0] if email_parts else ""
            subscriptor = Subscriptor(name=name,email=email)
            subscriptor.save()

        # Obtener la instancia de Teenvio o crear una nueva
        try:
            teenvio = Teenvio.objects.get_singleton()
        except Teenvio.DoesNotExist:
            # En caso de que no exista el modelo Teenvio, enviar el correo al correo auxiliar
            send_mail(
                'Nuevo suscriptor',
                f'Se ha suscrito un nuevo correo electrónico: {email}',
                settings.AUXILIARY_EMAIL,  # Dirección de correo electrónico del remitente
                [settings.AUXILIARY_EMAIL],  # Correo electrónico auxiliar
                fail_silently=True
            )

            response_data = {
                'success': True,
                'message': 'Subscripción exitosa (correo enviado al correo auxiliar)'
            }
            return JsonResponse(response_data)

        # Armar los parámetros de la solicitud
        payload = {
            'gid': teenvio.gid,
            'action': teenvio.action,
            'plan': teenvio.plan,
            'user': teenvio.user,
            'pass': teenvio.password,
            'email': email
        }

        # Realizar la petición a la API Teenvio
        url = teenvio.url
        response = requests.post(url, data=payload)

        # Verificar el resultado de la petición
        if response.status_code == 200 and 'OK' in response.text:
            # Éxito
            try:
                subscriptor = Subscriptor.objects.get(email=email)
                subscriptor.sincronizado = True
                subscriptor.save()
            except Subscriptor.DoesNotExist:
                pass
            response_data = {
                'success': True,
                'message': 'Subscripción exitosa'
            }
        else:
            # En caso de error, enviar el correo al correo auxiliar
            send_mail(
                'Error en suscripción',
                f'Hubo un error en la suscripción del correo electrónico: {email}',
                settings.AUXILIARY_EMAIL,  # Dirección de correo electrónico del remitente
                [settings.AUXILIARY_EMAIL],  # Correo electrónico auxiliar
                fail_silently=True
            )

            response_data = {
                'error': 'Error en la petición a Teenvio (correo enviado al correo auxiliar)'
            }

        # Devolver una respuesta JSON indicando el resultado
        return JsonResponse(response_data)