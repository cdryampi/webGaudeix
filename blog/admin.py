from django.contrib import admin
from .models import SubBlog, Categoria, GaleriaImagen, Fichero, Post, GaleriaImagenPost

class SubBlogAdmin(admin.ModelAdmin):
    pass

class FicheroInline(admin.TabularInline):
    model = Fichero
    extra = 1

class ImagenInline(admin.TabularInline):
    model = GaleriaImagen
    extra = 1

class CategoriaAdmin(admin.ModelAdmin):
    inlines = [ImagenInline]

class GaleriaImagenPostInline(admin.TabularInline):
    model = GaleriaImagenPost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [GaleriaImagenPostInline]

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubBlog, SubBlogAdmin)
#admin.site.register(Post, PostAdmin)