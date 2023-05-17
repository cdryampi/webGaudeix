from django.contrib import admin
from .models import Personalizacion

@admin.register(Personalizacion)
class PersonalizacionAdmin(admin.ModelAdmin):
    list_display = ['id']
    fieldsets = [
        ('Configuración General', {'fields': []}),
        ('Favicon', {'fields': ['favicon']}),
    ]
