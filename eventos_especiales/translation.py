from modeltranslation.translator import translator, TranslationOptions, register
from .models import EventoEspecial, MedidaEconomica, Mensaje, Autor


@register(EventoEspecial)
class EventoEspecialTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion_larga', 'descripcion_corta', 'boton_texto_google_form', 'titulo_google_form')  # Lista de campos que deseas traducir

@register(MedidaEconomica)
class MedidaEconomicaTranslationOptions(TranslationOptions):
    fields = ('titulo_html', 'descripcion')  # Lista de campos que deseas traducir

@register(Mensaje)
class MensajeTranslationOptions(TranslationOptions):
    fields = ('titulo', 'contenido', 'mensaje_despedida')  # Lista de campos que deseas traducir

@register(Autor)
class AutorTranslationOptions(TranslationOptions):
    fields = ('cargo',)  # Lista de campos que deseas traducir