from django.contrib import admin
from .models import Imagen



class ImagenAdmin(admin.ModelAdmin):

    model = Imagen


admin.site.register(Imagen, ImagenAdmin)

