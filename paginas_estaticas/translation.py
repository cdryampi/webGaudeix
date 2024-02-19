from modeltranslation.translator import translator, TranslationOptions, register
from .models import PaginaLegal, PuntoInformacion, Cookies, Contacto, Diversidad

# Define las opciones de traducción para el modelo Post
@register(PaginaLegal)
class PaginaLegalTranslationOptions(TranslationOptions):
    fields = ('titulo', 'encabezado','contenido')

@register(PuntoInformacion)
class PuntoInformacionTranslationOptions(TranslationOptions):
    fields = ('titulo','descripcion')

@register(Cookies)
class CookiesTranslationOptions(TranslationOptions):
    fields = ('titulo', 'contenido')

@register(Contacto)
class ContactoTranslationOptions(TranslationOptions):
    fields = ('titulo','subtitulo','descripcion')

@register(Diversidad)
class DiversidadTranslationOptions(TranslationOptions):
    fields = ('titulo','sub_titulo','descripcion_auxiliar')