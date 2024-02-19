from modeltranslation.translator import translator, TranslationOptions, register
from .models import TrenPersonalizacion, AutoPistaPersonalizacion, BusPersonalizacion, AeropuertoPersonalizacion


@register(TrenPersonalizacion)
class TrenPersonalizacionTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion',)  # Lista de campos que deseas traducir
