from modeltranslation.translator import translator, TranslationOptions, register
from .models import Personalizacion, TrenPersonalizacion, AutoPistaPersonalizacion, BusPersonalizacion, AeropuertoPersonalizacion, SuperDestacado, IframeVideoHome

@register(Personalizacion)
class PersonalizacionTranslationOptions(TranslationOptions):
    pass

@register(TrenPersonalizacion)
class TrenPersonalizacionTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion',)

@register(AutoPistaPersonalizacion)
class AutoPistaPersonalizacionTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion',)

@register(BusPersonalizacion)
class BusPersonalizacionTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion',)

@register(AeropuertoPersonalizacion)
class AeropuertoPersonalizacionTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion',)


@register(SuperDestacado)
class SuperDestacadoTranslationOptions(TranslationOptions):
    fields = ('titulo','descripcion',)

@register(IframeVideoHome)
class IframeVideoHomeTranslationOptions(TranslationOptions):
    fields = ('title' ,'description',)