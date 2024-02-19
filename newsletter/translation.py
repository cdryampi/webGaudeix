from modeltranslation.translator import translator, TranslationOptions, register
from .models import Newsletter

# Define las opciones de traducción para el modelo Post
@register(Newsletter)
class NewsletterTranslationOptions(TranslationOptions):
    fields = ('subtitulo','html_file')