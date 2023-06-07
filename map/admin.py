from .models import MapPoint
from django.contrib import admin
from .utils import export_map_points_csv



class MapPointAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'latitud', 'longitud', 'icono')
    list_filter = ('icono',)
    search_fields = ('titulo', 'latitud', 'longitud')
    actions = [export_map_points_csv]

admin.site.register(MapPoint, MapPointAdmin)
