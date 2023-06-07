import csv
from django.http import HttpResponse

def export_map_points_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="map_points.csv"'

    writer = csv.writer(response)
    writer.writerow(['Titulo', 'Latitud', 'Longitud', 'Icono'])

    for map_point in queryset:
        writer.writerow([map_point.titulo, map_point.latitud, map_point.longitud, map_point.icono])

    return response
export_map_points_csv.short_description = 'Exportar a CSV'
