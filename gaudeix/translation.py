from django.utils import translation
from django.conf import settings

class ForceDefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.default_language = getattr(settings, 'DEFAULT_LANGUAGE', 'ca')
    
    def __call__(self, request):
        user_language = request.COOKIES.get('django_language', self.default_language)
        translation.activate(user_language)
        request.LANGUAGE_CODE = user_language
        response = self.get_response(request)
        if 'django_language' not in request.COOKIES:
            response.set_cookie('django_language', user_language)
        return response
