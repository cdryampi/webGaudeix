from django.contrib import admin
from .models import Imagen, Fichero, Video



class ImagenAdmin(admin.ModelAdmin):
    model = Imagen
    readonly_fields = ['modelo_asociado']


    

    def modelo_asociado(self, instance):
        if instance.subblogimagen:
            return instance.subblogimagen.subblog._meta.verbose_name
        elif instance.categoriabannerimagen:
            return instance.categoriabannerimagen.categoria._meta.verbose_name
        elif instance.categoriagaleriaimagen:
            return instance.categoriagaleriaimagen.categoria._meta.verbose_name
        elif instance.postimagen:
            return instance.postimagen.post._meta.verbose_name
        elif instance.postgaleriaimagen:
            return instance.postgaleriaimagen.post._meta.verbose_name
        else:
            return '-'

    modelo_asociado.short_description = 'Modelo Asociado'

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'subblogimagen' or db_field.name == 'categoriabannerimagen' or db_field.name == 'categoriagaleriaimagen' or db_field.name == 'postimagen' or db_field.name == 'postgaleriaimagen':
    #         kwargs['queryset'] = Imagen.objects.exclude(
    #             subblogimagen__isnull=False,
    #             categoriabannerimagen__isnull=False,
    #             categoriagaleriaimagen__isnull=False,
    #             postimagen__isnull=False,
    #             postgaleriaimagen__isnull=False,
    #         )
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FicheroAdmin(admin.ModelAdmin):
    model = Fichero

class VideoAdmin(admin.ModelAdmin):
    model = Video

admin.site.register(Fichero, FicheroAdmin)

admin.site.register(Imagen, ImagenAdmin)
admin.site.register(Video, VideoAdmin)



