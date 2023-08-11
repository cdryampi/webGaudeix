from .models import Header, Referencia, EnlaceExterno, HeaderFooter
from django.contrib import admin


class EnlaceExternoInline(admin.StackedInline):
    model = EnlaceExterno
    extra = 1


class ReferenciaAdmin(admin.TabularInline):
     model = Referencia

@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
     inlines = [ReferenciaAdmin]
@admin.register(HeaderFooter)
class HeaderFooterAdmin(admin.ModelAdmin):
     inlines = [ReferenciaAdmin]

@admin.register(Referencia)  # Quita el comentario para registrar el modelo Referencia
class ReferenciaAdminWeb(admin.ModelAdmin):
     pass

@admin.register(EnlaceExterno)
class EnlaceExternoAdminWeb(admin.ModelAdmin):
     pass
