from django.contrib import admin
from .models import Newsletter
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import activate, get_language, deactivate
from django.utils.html import format_html_join
from django.conf import settings



class NewsletterAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('nombre_interno', 'evento_especial', 'html_file')
    search_fields = ('nombre_interno', 'evento_especial__titulo')
    actions = ['generar_html_para_todos_los_idiomas']
    fieldsets = [
        (None, {
            'fields': [
                'evento_especial',
                'nombre_interno',
                'link_tracking',
                'subtitulo',
                'html_file'
                
            ],
            'description': (
                "<p><strong>Aquesta és la pàgina d'edició d'una plantilla de una Newsletter.</strong></p>"
                "<p><em>Les <u>Newsletter</u> serveix per poder generar una plantilla HTML per facilitar l'enviament una notificació pels subscriptors amb una eina externa.</em></p>"
                "<p>Assegura't d'adaptar la plantilla si cal.</p>"
                "<p>Els enllaços del tracking estan limitats pels logos de la web. Una vegada generada la plantilla el pots modificar manualment els enllaços. Però cal que l'enllaç arribi cap a la web.</p>"
                "<p>El subtítol és per poder afegir un nom de l'esdeveniment especial, ha de tenir relació amb la temàtica.</p>"
                "<p><strong>Nota:</strong> Pots esborrar totes les plantilles des de Personalització, així no omplim el servidor de fitxers innecessaris.</p>"
                "<p>Pots tornar a generar la plantilla tantes vegades com vulguis des del llistat de newsletter.</p>"
            ),
        }),
    ]
    readonly_fields = ['html_file']
    def generar_html_para_todos_los_idiomas(self, request, queryset):

        for newsletter in queryset:
            newsletter.generar_y_guardar_html()
        self.message_user(request, "HTML generado para todos los idiomas.")


    generar_html_para_todos_los_idiomas.short_description = "Generar HTML para todos los idiomas"


admin.site.register(Newsletter, NewsletterAdmin)
