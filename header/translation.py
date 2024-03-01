from modeltranslation.translator import translator, TranslationOptions, register
from .models import EnlaceExterno

# Define las opciones de traducción para el modelo Post
@register(EnlaceExterno)
class EnlaceExternoTranslationOptions(TranslationOptions):
    fields = ('titulo',)