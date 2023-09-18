from django.contrib import admin
from .models import SeleccionDestacados
from .forms import SeleccionForm

# Register your models here.

class SeleccionDestacadosAdmin(admin.ModelAdmin):
    form = SeleccionForm  # Usar el formulario de Posts
    autocomplete_fields = ['eventos_especiales']
    
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'coleccion',
                'eventos_especiales',
                'publicado',
                ],

            'description': (
                "<p><strong><em>Aquesta és l'administració d'una Selecció de continguts.</em></strong></p>"
                "<p><em>En aquesta secció, pots gestionar els elements que apareixeran a la portada del teu lloc web utilitzant un carrousel anomenat <i>Swipper</i>. És una manera eficaç de destacar i presentar les entrades, com ara publicacions, visites guiades, rutes, llocs d'interès i molt més.</em></p>"
                "<p><em>Assegura't de no sobrecarregar amb massa elements, ja que això podria afectar negativament el temps de carrega i l'experiència de l'usuari a la pàgina d'inici.</em></p>"
                "<p><em>Aquests camps estan dissenyats per a recopilar la informació necessària per al <i>Swipper</i> de la pàgina d'inici, per tant, omple'ls amb cura per garantir que els teus continguts destacats es presentin de manera atractiva i efectiva.</em></p>"
                "<p><em>Cal tenir en compte que només es mostrarà la primera selecció que estigui publicada. Per tant, assegura't de mantenir només les seleccions que vulguis destacar a la pàgina d'inici amb l'estat 'publicat'.</em></p>"
            ),
        }),
        # Resto de los fieldsets
    ]

admin.site.register(SeleccionDestacados, SeleccionDestacadosAdmin)