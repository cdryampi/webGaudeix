from .models import Header, Referencia
from django.contrib import admin

class ReferenciaAdmin(admin.TabularInline):
     model = Referencia

@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
     inlines = [ReferenciaAdmin]
