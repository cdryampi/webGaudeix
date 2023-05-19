from django.contrib import admin
from .models import Imagen



class ImagenAdmin(admin.ModelAdmin):
    model = Imagen
    readonly_fields = ['modelo_asociado']

    def modelo_asociado(self, instance):
        
        if instance.subblogimagen:
            return instance.subblogimagen.subblog.__class__.__name__
        elif instance.categoriabannerimagen:
            return instance.categoriabannerimagen.categoria.__class__.__name__
        elif instance.categoriagaleriaimagen:
            return instance.categoriagaleriaimagen.categoria.__class__.__name__
        else:
            return '-'

    modelo_asociado.short_description = 'Modelo Asociado'


admin.site.register(Imagen, ImagenAdmin)

