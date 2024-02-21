from modeltranslation.translator import translator, TranslationOptions, register
from .models import Personalizacion, TrenPersonalizacion, AutoPistaPersonalizacion, BusPersonalizacion, AeropuertoPersonalizacion

@register(Personalizacion)
class PersonalizacionTranslationOptions(TranslationOptions):
    pass

@register(TrenPersonalizacion)
class TrenPersonalizacionTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion',)  # Lista de campos que deseas traducir

@register(AutoPistaPersonalizacion)
class AutoPistaPersonalizacionTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion',)  # Lista de campos que deseas traducir

@register(BusPersonalizacion)
class BusPersonalizacionTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion',)  # Lista de campos que deseas traducir

@register(AeropuertoPersonalizacion)
class AeropuertoPersonalizacionTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion',)  # Lista de campos que deseas traducir