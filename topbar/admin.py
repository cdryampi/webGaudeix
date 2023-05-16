from django.contrib import admin
from .models import Topbar

@admin.register(Topbar)
class TopbarAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'descripcion', 'descripcion_corta_movil', 'enlace_externo']
