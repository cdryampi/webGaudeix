from django.contrib import admin
from .models import Teenvio, Subscriptor
from django.http import HttpResponse
import csv
# Register your models here.
@admin.register(Teenvio)
class TeenvioAdmin(admin.ModelAdmin):
    list_display = ['gid', 'user', 'plan']





@admin.register(Subscriptor)
class SubscriptorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']  # Mostrar campos en la lista del admin

    def formatted_email(self, obj):
        return f'\t{obj.email}'  # Agrega una tabulación al inicio del correo electrónico
    
    def export_subscribers_to_csv(modeladmin,request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Fecha de creación'])  # Encabezados de las columnas
        
        for subscriber in queryset:
            if subscriber.exportable:
                writer.writerow([subscriber.name, subscriber.email, subscriber.created_at])
        return response
    export_subscribers_to_csv.short_description = 'Exporta els subcriptors seleccionats a CSV'

    actions = [export_subscribers_to_csv]  # Agregar la acción personalizada