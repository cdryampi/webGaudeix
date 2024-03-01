from django.contrib import admin
from .models import RedSocial

class RedSocialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'link', 'fondo')
    fieldsets = [
        (None, {
            'fields': ['titulo', 'imagen', 'link', 'fondo', 'orden'],
            'description': (
                "<p><strong><em>Gestió de Xarxes Socials</em></strong></p>"
                "<p>Aquesta secció permet afegir, modificar i visualitzar les xarxes socials associades amb el lloc web. Cada xarxa social pot ser representada per un títol, una imatge (preferiblement el logotip), un enllaç directe al perfil o pàgina, i un color de fons específic.</p>"
                "<p>El <em>títol</em> identifica la xarxa social, mentre que l'<em>imatge</em> hauria de ser una representació visual clara i reconeixible.</p>"
                "<p>El camp <em>enllaç</em> és essencial per a dirigir els usuaris cap a la xarxa social corresponent.</p>"
                "<p>El <em>color de fons</em> es pot utilitzar per personalitzar l'aparença de la xarxa social en el lloc web, com en un TopBar o elements similars.</p>"
                "<p>Assegura't d'actualitzar aquestes dades amb precisió per a assegurar una representació adequada de les xarxes socials en el teu lloc web.</p>"
                "<p><strong>Nota:</strong> Les imatges han de ser en blanc amb fons transparent per assegurar la seva correcta visualització amb qualsevol estil del lloc web.</p>"
            ),
        }),
    ]


admin.site.register(RedSocial, RedSocialAdmin)