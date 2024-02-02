from modeltranslation.translator import translator, TranslationOptions, register
from .models import MapPoint


@register(MapPoint)
class MapPointranslationOptions(TranslationOptions):
    pass
