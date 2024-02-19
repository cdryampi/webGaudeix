from modeltranslation.translator import translator, TranslationOptions, register
from .models import CompraDescubre, CompraDescubrePasosImagen


@register(CompraDescubre)
class CompraDescubreTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion_larga', 'descripcion_corta')  # Lista de campos que deseas traducir

@register(CompraDescubrePasosImagen)
class CompraDescubrePasosImagenTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion')
