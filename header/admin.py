from .models import Header, Referencia, EnlaceExterno
from django.contrib import admin


class EnlaceExternoInline(admin.StackedInline):
    model = EnlaceExterno
    extra = 1


class ReferenciaAdmin(admin.TabularInline):
     model = Referencia

@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
     inlines = [ReferenciaAdmin]




@admin.register(Referencia)
class ReferenciaAdminWeb(admin.ModelAdmin):
    inlines = [EnlaceExternoInline]