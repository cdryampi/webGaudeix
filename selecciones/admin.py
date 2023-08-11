from django.contrib import admin
from .models import SeleccionDestacados
from .forms import SeleccionForm

# Register your models here.

class SeleccionDestacadosAdmin(admin.ModelAdmin):
    form = SeleccionForm  # Usar el formulario de Posts
    autocomplete_fields = ['eventos_especiales']

admin.site.register(SeleccionDestacados, SeleccionDestacadosAdmin)