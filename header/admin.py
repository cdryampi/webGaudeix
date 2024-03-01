from .models import Header, Referencia, EnlaceExterno, HeaderFooter
from modeltranslation.admin import TranslationAdmin

from django.contrib import admin


class EnlaceExternoInline(admin.StackedInline):
    model = EnlaceExterno
    extra = 1


class ReferenciaAdmin(admin.TabularInline):
     model = Referencia

     autocomplete_fields = ('post','categoria','subblog','evento_especial')


     def get_formset(self, request, obj=None, **kwargs):
          formset = super().get_formset(request, obj, **kwargs)

          if isinstance(self.admin_site._registry.get(Header), HeaderAdmin):
               formset.form.base_fields['header_footer'].queryset = HeaderFooter.objects.none()

          if isinstance(self.admin_site._registry.get(HeaderFooter), HeaderFooterAdmin):
               formset.form.base_fields['header'].queryset = Header.objects.none()

          return formset
 #    fields = ['tipo','post','categoria','subblog','externo','contacto','evento_especial','orden','subvencion']

@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
     inlines = [ReferenciaAdmin]
     
     fieldsets = [
        (None, {
            'fields': [
                'logo',
                'color_fondo_header',
                'color_letra',
                'color_entrada'
            ],
               'description': (
                    "<p><strong>Aquesta és la pàgina d'edició de la capçalera superior.</strong></p>"
                    "<p>Afegeix un logotip sense fons o juga amb els colors de la capçalera.</p>"
                    "<p>Tingues en compte els colors que fas servir; el text de la capçalera ha de ser llegible.</p>"
                    "<p><em>Pots seleccionar el tipus de referència que vols tenir a la capçalera superior del lloc web.</em></p>"
                    "<p>Tingues en compte que una referència només pot tenir una sola vinculació.</p>"
                    "<p><em>Assegura't d'afegir referències que consideris rellevants.</em></p>"
                    "<p><em>Les <strong>referències</strong> que es generen automàticament s'han d'eliminar si no les fas servir per evitar problemes en desar-les.</em></p>"
                    "<p><em>PD: Volem destacar les entrades per facilitar a la gent trobarla, aixì que s'ha de afegir un color adicional.</em></p>"
               ),

        }),
        # Otras secciones de fieldsets aquí si es necesario
    ]
     
@admin.register(HeaderFooter)
class HeaderFooterAdmin(admin.ModelAdmin):
     inlines = [ReferenciaAdmin]
     
     fieldsets = [
        (None, {
            'fields': [
                'color_fondo_header',
                'color_letra',
            ],
               'description': (
                    "<p><strong>Aquesta és la pàgina d'edició de la capçalera inferior.</strong></p>"
                    "<p><em>Pots seleccionar el tipus de referència que vols tenir a la capçalera inferior del lloc web.</em></p>"
                    "<p>Afegeix un logotip sense fons o juga amb els colors de la capçalera.</p>"
                    "<p>Tingues en compte els colors que fas servir; el text de la capçalera ha de ser llegible.</p>"
                    "<p>Tingues en compte que una referència només pot tenir una sola vinculació.</p>"
                    "<p><em>Assegura't d'afegir referències que consideris rellevants.</em></p>"
                    "<p><em>Les <strong>referències</strong> que es generen automàticament s'han d'eliminar si no les fas servir per evitar problemes en desar-les.</em></p>"
               ),

        }),
        # Otras secciones de fieldsets aquí si es necesario
    ]

@admin.register(Referencia)  # Quita el comentario para registrar el modelo Referencia
class ReferenciaAdminWeb(admin.ModelAdmin):
     pass

@admin.register(EnlaceExterno)
class EnlaceExternoAdminWeb(TranslationAdmin, admin.ModelAdmin):
     fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'enlace',
                'color_letra',
                'estil_del_text'
            ],
               'description': (
                    "<p><strong>Aquesta és la pàgina d'edició d'un enllaç extern.</strong></p>"
                    "<p><em>En aquests enllaços pots afegir referències externes cap a altres webs.</em></p>"
                    "<p><em>Els camps són obligatoris i has de posar el títol i l'enllaç.</em></p>"
               ),

        }),
        # Otras secciones de fieldsets aquí si es necesario
    ]
