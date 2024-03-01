from modeltranslation.translator import translator, TranslationOptions, register
from .models import Parallax, ImagenCarrusel, Carrusel

@register(Parallax)
class ParallaxTranslationOptions(TranslationOptions):
    fields = ('descripcion_corta',)

@register(Carrusel)
class CarruselTranslationOptions(TranslationOptions):
    pass

@register(ImagenCarrusel)
class ImagenCarruselTranslationOptions(TranslationOptions):
    fields = ('descripcion',)
