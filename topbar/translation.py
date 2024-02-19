from modeltranslation.translator import translator, TranslationOptions, register
from .models import Topbar


@register(Topbar)
class TopbarTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion', 'descripcion_corta_movil', 'titulo_externo')  # Lista de campos que deseas traducir