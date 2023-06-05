from .models import MapPoint
from django.contrib import admin




class MapPointAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'latitud', 'longitud', 'icono')
    list_filter = ('icono',)
    search_fields = ('titulo', 'latitud', 'longitud')

admin.site.register(MapPoint, MapPointAdmin)
