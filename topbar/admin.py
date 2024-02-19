from django.contrib import admin
from .models import Topbar
from modeltranslation.admin import TranslationAdmin

@admin.register(Topbar)
class TopbarAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ['titulo', 'descripcion', 'descripcion_corta_movil', 'enlace_externo']
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'descripcion',
                'descripcion_corta_movil',
                'enlace_externo',
                'titulo_externo',
                'fondo',
                'texto_color',
                'publicado',
            ],
            'description': (
                "<p><strong><em>Aquesta és l'administració d'un TopBar.</em></strong></p>"
                "<p><em>Aquí pots introduir totes les dades relacionades amb el teu TopBar."
                "Assegura't d'omplir tots els camps necessaris amb la informació correcta.</em></p>"
                "<p><em>El TopBar és una barra que apareix en la part superior de la teva pàgina web."
                "El seu principal propòsit és proporcionar una manera fàcil d'afegir informació destacada o enllaços importants per als teus usuaris.</em></p>"
                "<p><em>Assegura't de tenir només un TopBar actiu alhora. Si vols que el teu TopBar es mostri, assegura't que els altres estiguin despublicats, ja que el sistema només acceptarà el primer TopBar publicat. D'aquesta manera, evitaràs resultats no desitjats i garantiràs que el teu TopBar sigui visible per als teus usuaris.</em></p>"
            ),
        }),
    ]
