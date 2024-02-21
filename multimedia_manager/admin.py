from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Imagen, Fichero, Video, Parallax, VideosEmbed, Audio



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

class ParallaxAdmin(TranslationAdmin, admin.ModelAdmin):
    model = Parallax

class VideosEmbedAdmin(admin.ModelAdmin):
    model = VideosEmbed

class AudioAdmin(admin.ModelAdmin):
    model = Audio


admin.site.register(Fichero, FicheroAdmin)
admin.site.register(Imagen, ImagenAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Parallax, ParallaxAdmin)
admin.site.register(VideosEmbed, VideosEmbedAdmin)
admin.site.register(Audio, AudioAdmin)