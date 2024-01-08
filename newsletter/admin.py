from django.contrib import admin
from .models import Newsletter
from django.utils.safestring import mark_safe
from django.utils.html import format_html


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('nombre_interno', 'evento_especial', 'html_file')
    search_fields = ('nombre_interno', 'evento_especial__titulo')
    actions = ['generar_html_para_newsletters_seleccionadas']
    fieldsets = [
        (None, {
            'fields': [
                'evento_especial',
                'nombre_interno',
                'generar_plantilla',
                'link_tracking',
                'subtitulo',
                
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
    readonly_fields = ['generar_plantilla','html_file']


    def generar_plantilla(self, obj):
        if obj.html_file:
            # Si el archivo existe, genera el enlace de descarga
            file_path = obj.html_file.path
            download_link = format_html('<a href="{}" download="{}">Baixar HTML</a>', obj.html_file.url, file_path)
            return download_link
        else:
            # Si el archivo no existe, genera y guarda el HTML
            obj.generar_y_guardar_html()
            # Recargar el objeto para asegurarse de que 'html_file' esté actualizado
            obj.refresh_from_db()
            if obj.html_file:
                file_path = obj.html_file.path
                download_link = format_html('<a href="{}" download="{}">Baixar HTML</a>', obj.html_file.url, file_path)
                return download_link
            else:
                # En caso de que el archivo siga sin existir después de intentar generarlo
                return "Fitxer no disponible"
        
    generar_plantilla.allow_tags = True
    generar_plantilla.short_description = 'Generar HTML'

    def generar_html_para_newsletters_seleccionadas(self, request, queryset):
        for newsletter in queryset:
            newsletter.generar_y_guardar_html()
        self.message_user(request, "La plantilla HTML s'ha generat bé.")
    generar_html_para_newsletters_seleccionadas.short_description = "Generar plantilles HTML per les newsletters seleccionades"

admin.site.register(Newsletter, NewsletterAdmin)
