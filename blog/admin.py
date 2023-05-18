from django.contrib import admin
from .models import SubBlog, Categoria, GaleriaImagen, Fichero, Post, GaleriaImagenPost, SubBlogImagen
from multimedia_manager.models import Imagen

class ImagenInline(admin.TabularInline):
    model = Imagen

class SubBlogImagenInline(admin.TabularInline):
    model = SubBlogImagen
    inlines = [ImagenInline]

class SubBlogAdmin(admin.ModelAdmin):
    inlines = [SubBlogImagenInline]



class FicheroInline(admin.TabularInline):
    model = Fichero
    extra = 1

class ImagenInline(admin.TabularInline):
    model = GaleriaImagen
    extra = 1

# class CategoriaAdmin(admin.ModelAdmin):
#     inlines = [ImagenInline]

# class GaleriaImagenPostInline(admin.TabularInline):
#     model = GaleriaImagenPost


# admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubBlog, SubBlogAdmin)
admin.site.register(Imagen)
#admin.site.register(Post, PostAdmin)