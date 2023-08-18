from .models import Header, Referencia, EnlaceExterno, HeaderFooter
from django.contrib import admin


class EnlaceExternoInline(admin.StackedInline):
    model = EnlaceExterno
    extra = 1


class ReferenciaAdmin(admin.TabularInline):
     model = Referencia
     autocomplete_fields = ['post','categoria','subblog','evento_especial',]


     def get_formset(self, request, obj=None, **kwargs):
          formset = super().get_formset(request, obj, **kwargs)

          if isinstance(self.admin_site._registry.get(Header), HeaderAdmin):
               formset.form.base_fields['header_footer'].queryset = HeaderFooter.objects.none()

          if isinstance(self.admin_site._registry.get(HeaderFooter), HeaderFooterAdmin):
               formset.form.base_fields['header'].queryset = Header.objects.none()

          return formset

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
