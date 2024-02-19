from modeltranslation.translator import translator, TranslationOptions, register
from .models import Alerta


@register(Alerta)
class AlertaTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion')  # Lista de campos que deseas traducir