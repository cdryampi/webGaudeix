from modeltranslation.translator import translator, TranslationOptions, register
from .models import Parallax

@register(Parallax)
class ParallaxTranslationOptions(TranslationOptions):
    fields = ('descripcion_corta',)

