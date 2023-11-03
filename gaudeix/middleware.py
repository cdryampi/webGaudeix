import json
import traceback
from admin_utils.models import RegistroError  # Importa el modelo
import sys

class LogError500Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Verifica si la respuesta es un error 500
        if response.status_code == 500:
            # Captura el tipo de error si está disponible
            error_type = self.get_error_type(response)

            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_info = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))

            # Establece un título o nombre clave basado en el tipo de error
            if error_type:
                error_title = f"{error_type}"
            else:
                error_title = "Error 500 interno del servidor"


            # Registra los detalles del error en el modelo RegistroError
            error_details = {
                'titulo': error_title,
                'descripcion': traceback.format_exc(),
                'nota': '',
                'resuelto': False,
            }
            RegistroError.objects.create(**error_details)

        return response

    def get_error_type(self, response):
        try:
            # Captura el tipo de error si está disponible
            # Aquí asumimos que el tipo de error se encuentra en el contenido HTML de la respuesta
            content = response.content.decode('utf-8')
            # Puedes personalizar cómo extraer el tipo de error según la estructura de tu aplicación
            # Por ejemplo, si tu aplicación devuelve JSON en caso de error:
            # error_data = json.loads(content)
            # return error_data.get('error_type', '')

            # Aquí asumimos que la descripción del error contiene información sobre el tipo
            # Puedes ajustar esto según tus necesidades
            if 'KeyError' in content:
                return 'KeyError'
            elif 'ValueError' in content:
                return 'ValueError'
            # Agrega más condiciones según los tipos de error que desees capturar
            else:
                return None  # Si no se encuentra un tipo de error específico

        except Exception as e:
            return None  # En caso de cualquier error, devuelve None

    def get_error_description(self, response):
        try:
            # Intenta obtener la descripción del error desde el contenido de la respuesta
            content = response.content.decode('utf-8')
            # Puedes personalizar cómo extraer la descripción según la estructura de tu aplicación
            # Por ejemplo, si tu aplicación devuelve JSON en caso de error:
            # error_data = json.loads(content)
            # return error_data.get('description', '')

            # Aquí asumimos que la descripción está en el contenido HTML de la respuesta
            return content
        except Exception as e:
            return str(e)
