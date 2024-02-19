from django.utils import translation

class ForceDefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if 'django_language' not in request.COOKIES:
            # Forzar catalán como idioma por defecto
            user_language = 'ca'
            translation.activate(user_language)
            request.LANGUAGE_CODE = user_language
            response = self.get_response(request)
            response.set_cookie('django_language', user_language)
        else:
            # Usar el idioma configurado por el usuario
            user_language = request.COOKIES.get('django_language')
            translation.activate(user_language)
            request.LANGUAGE_CODE = user_language
            response = self.get_response(request)
        return response
