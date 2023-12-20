from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import RegistroError
from django.core.files.storage import default_storage
from multimedia_manager.models import Imagen, Fichero, Video



@admin.register(RegistroError)
class RegistroErrorAdmin(admin.ModelAdmin):


    fieldsets = [
        (None, {
            'fields': [
                'descripcion',
                'nota',
                'resuelto'
            ],
            'description': (
                "<p><strong><em>Aquesta és l'administració de la gestió dels errors de la web.</em></strong></p>"
                "<p><em>Pots agafar un error i sàpiga que ha passat i els pots corregir el problema si pots.</em></p>"
                "<p><em>L'error més comú són les imatges, tens una funcionalitat per eliminar totes les referències corruptes.</em></p>"
                "<p>Selecciona totes les referències o el quadrat superior i a continuació fes servir el desplegable i selecciona 'Eliminar les imatges sense fitxers' una vegada fet tot això fes clic al botó 'anar'.</p>"
            )
        })
    ]


    list_display = ('fecha', 'titulo','resuelto')
    list_filter = ('fecha', 'resuelto')
    search_fields = ('mensaje',)
    date_hierarchy = 'fecha'
    readonly_fields = ('descripcion','fecha')


    def delete_records_with_missing_files(self, request, queryset):
        imagenes = Imagen.objects.all()
        deleted_count = 0
        for imagen in imagenes:
            if not imagen.archivo or not imagen.archivo.storage.exists(imagen.archivo.name):
                imagen.delete()
                deleted_count += 1

        if deleted_count == 1:
            message_bit = "1 registre s'ha eliminat."
        else:
            message_bit = f"{deleted_count} registres s'han eliminat."
        self.message_user(request, f"{message_bit} registres sense fitxers relacionats.")

    delete_records_with_missing_files.short_description = "Eliminar les imatges sense fitxers"

    
    actions = [delete_records_with_missing_files]
    actions_on_top = True 