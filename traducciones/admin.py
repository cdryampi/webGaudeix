from django.contrib import admin
from .models import Translation
from django.urls import reverse
from django.utils.html import format_html



@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ['language_code']
    fieldsets = [
        (None, {
            'fields': [
                'language_code',
                'custom_change_view_button'
            ],
            'description': (
                            "<p><strong>Informació sobre les traduccions i els fitxers .po:</strong></p>"
                            "<p>Les traduccions en aquest sistema es gestionen a través de fitxers .po, que són fitxers de text utilitzats per la localització de software. Cada fitxer .po conté parelles de text original (msgid) i la seva traducció (msgstr) en un idioma específic.</p>"
                            "<p>Quan tradueixes contingut en el sistema, estàs modificant els fitxers .po associats amb cada idioma. Aquests canvis no són efectius immediatament en la web; primer han de ser compilats en fitxers .mo, que són els que Django utilitza per carregar les traduccions en l'aplicació.</p>"
                            "<p><strong>Com a funcionar:</strong></p>"
                            "<ul>"
                                "<li>Per afegir una nova traducció, busca la cadena original (msgid) i afegeix la traducció corresponent (msgstr) en el fitxer .po de l'idioma desitjat.</li>"
                                "<li>Una vegada hagis fet els canvis en els fitxers .po, la funcionalitat de 'compilar traduccions' s'encarregarà de generar els fitxers .mo necessaris.</li>"
                                "<li>És important recordar que qualsevol error en la sintaxi dels fitxers .po pot provocar que les traduccions no es compilen correctament, afectant la disponibilitat de les traduccions en la web.</li>"
                            "</ul>"
                            "<p><strong>Advertència:</strong> Sigues cautelós al editar fitxers .po directament i sempre assegura't de validar la sintaxi abans de compilar les traduccions. Si no estàs segur, demana ajuda a un desenvolupador.</p>"
                            "<p>Aquesta funcionalitat de traduccions és una eina poderosa per gestionar contingut multilingüe, permetent que la web sigui accessible a una audiència global més àmplia.</p>"
            ),
        }),
    ]
    readonly_fields =['custom_change_view_button']

    def custom_change_view_url(self, obj):
        if obj.id is not None:
            return reverse('translation-edit', args=[obj.pk])

    def custom_change_view_button(self, obj):
        url = self.custom_change_view_url(obj)
        if obj.id is not None:
            return format_html('<a class="button" href="{}">Editar Traducció </a>', url)
        return "Primer has de guardar per poder editar."
    custom_change_view_button.short_description = "Editar Traducció"