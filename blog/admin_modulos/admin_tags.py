from django.contrib import admin

class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'nombre',
                # Otros campos del modelo de Tag aquí
            ],
            'description': (
                "<p><strong><em>Aquest és l'administració d'un Tag.</em></strong></p>"
                "<p><em>Introdueix el nom del Tag en el camp 'Nom'. Assegura't d'utilitzar un nom significatiu "
                "i rellevant per a aquest Tag.</em></p>"
                "<p><em>Els Tags són utilitzats per agrupar esdeveniments relacionats en la teva Agenda. Pots utilitzar-los "
                "per organitzar esdeveniments per temes, tipus d'activitats o altres criteris.</em></p>"
                "<p><em>Quan generis un PDF de la teva Agenda, els Tags et permetran agrupar esdeveniments semblants o temàtiques, "
                "facilitant la cerca i navegació pels usuaris.</em></p>"
            ),
        }),
        # Resto de los fieldsets
    ]