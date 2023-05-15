from django.contrib import admin
from .models import PaginaLegal
# Register your models here.
@admin.register(PaginaLegal)
class PaginaLegalAdmin(admin.ModelAdmin):
    pass