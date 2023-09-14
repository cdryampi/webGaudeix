from django.contrib import admin
from .models import  PuntoInformacion, Contacto
from .models import PaginaLegal, Cookies

# Register your models here.
@admin.register(PaginaLegal)
class PaginaLegalAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'contenido',
                'imagen',
                'encabezado',
                'tipo',
            ],
            'description': (
                "<p><strong><em>Aquesta és l'administració d'una Pàgina Legal.</em></strong></p>"
                "<p><em>Aquí pots introduir totes les dades relacionades amb la teva pàgina legal. "
                "Assegura't d'omplir tots els camps necessaris amb la informació correcta.</em></p>"
                "<p><em>Aquesta pàgina pot contenir informació com la <strong>política de privacitat</strong>, "
                "l'<strong>avís legal</strong> o la <strong>política de cookies</strong>.</em></p>"
                "<p><em>Afegeix el <strong>títol</strong> de la pàgina, un possible <strong>encapçalament</strong>, una <strong>imatge</strong> i el seu <strong>contingut</strong>.</em></p>"
                "<p><em>Assegura't de seleccionar el <strong>tipus</strong> de la pàgina legal: "
                "<strong>Política de privacitat</strong>, <strong>Avís legal</strong> o <strong>Política de cookies</strong>.</em></p>"
                "<p><strong><em>Nota:</em></strong> Només es pot tenir una instància de cada tipus de pàgina legal. Si ja existeix una pàgina legal d'aquest tipus, no podràs crear-ne una altra.</p>"
                "<p><strong><em>Metadades i SEO:</em></strong> Les metadades són dades ocultes que es fan servir per millorar la visibilitat de la pàgina als motors de cerca com Google. Assegura't de que els camps com el <strong>títol</strong> i la <strong>descripció</strong> estiguin ben definits per atraure més usuaris a la teva pàgina.</p>"
            ),
        }),
    ]


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'banner',
                'subtitulo',
                'descripcion',
            ],
            'description': (
                "<p><strong><em>Aquesta és l'administració de la pàgina de contacte.</em></strong></p>"
                "<p><em>Aquí pots introduir totes les dades relacionades amb la pàgina de contacte. "
                "Assegura't d'omplir tots els camps necessaris amb la informació correcta.</em></p>"
                "<p><em>Recorda que aquests camps estan destinats a recollir informació sobre la pàgina de contacte, "
                "com el <strong>títol</strong>, el <strong>banner</strong>, el <strong>subtítol</strong>, "
                "i la <strong>descripció</strong>.</em></p>"
            ),
        }),
    ]


@admin.register(PuntoInformacion)
class PuntoInformacionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'telefono',
                'correo',
                'direccion',
                'banner',
                'descripcion',
                'mapa',
            ],
            'description': (
                "<p><strong><em>Aquesta és l'administració del Punt d'Informació Turística.</em></strong></p>"
                "<p><em>Aquí pots introduir totes les dades relacionades amb el punt d'informació turística. "
                "Assegura't d'omplir tots els camps necessaris amb la informació correcta.</em></p>"
                "<p><em>Recorda que aquests camps estan destinats a recollir informació sobre el punt d'informació, "
                "com el <strong>títol</strong>, el <strong>telèfon</strong>, el <strong>correu electrònic</strong>, "
                "la <strong>adreça</strong>, el <strong>banner</strong>, la <strong>descripció</strong>, i el <strong>mapa</strong>.</em></p>"
                "<p><em>Pots afegir una ubicació al punt d'informació mitjançant el camp <strong>Mapa</strong>.</em></p>"
            ),
        }),
    ]
    autocomplete_fields = ['mapa']

@admin.register(Cookies)
class CookiesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'contenido',
            ],
            'description': (
                "<p><strong><em>Aquesta és l'administració de la Política de Cookies.</em></strong></p>"
                "<p><em>Aquí pots definir el text i les condicions de la política de cookies que serà mostrada als usuaris.</em></p>"
                "<p><em>Assegura't de proporcionar una explicació clara i detallada sobre les cookies i com es faran servir.</em></p>"
                "<p><em>Aquesta política és important per obtenir el consentiment dels usuaris per a l'ús de les cookies. Encara que no fem servir cap</em></p>"
            ),
        }),
    ]

