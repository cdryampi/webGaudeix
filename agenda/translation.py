from modeltranslation.translator import translator, TranslationOptions, register
from .models import Agenda, Ruta, VisitaGuiada, Alojamiento, Restaurante


@register(Agenda)
class AgendaTranslationOptions(TranslationOptions):
    fields = ('descripcion_corta',)  # Lista de campos que deseas traducir

@register(Ruta)
class RutaTranslationOptions(TranslationOptions):
    fields = ('tema', 'actividad', 'tipologia', 'dificultad')

@register(VisitaGuiada)
class VisitaGuiadaTranslationOptions(TranslationOptions):
    pass

@register(Alojamiento)
class AlojamientoTranslationOptions(TranslationOptions):
    pass

@register(Restaurante)
class RestauranteTranslationOptions(TranslationOptions):
    fields = ('descripcion_corta',)