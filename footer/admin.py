from django.contrib import admin
from .models import Footer, FooterEmpresa, FooterInformacion

class FooterEmpresaInline(admin.StackedInline):
    model = FooterEmpresa
    extra = 1

class FooterInformacionInline(admin.StackedInline):
    model = FooterInformacion
    extra = 1

@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    inlines = [FooterEmpresaInline, FooterInformacionInline]
