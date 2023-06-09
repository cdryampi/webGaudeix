from django.contrib import admin
from .models import Categoria
from .models import  Categoria, SubBlog, Post, Tag, Noticia
from .admin_modulos.admin_subblog import SubBlogAdmin
from .admin_modulos.admin_categoria import CategoriaAdmin
from .admin_modulos.admin_post import PostAdmin
from .admin_modulos.admin_noticia import NoticiaAdmin
# Se define una clase inline para mostrar imágenes en línea en el admin




    
# Se registra el modelo Categoria en el admin con su configuración
admin.site.register(Categoria, CategoriaAdmin)

# Se registra el modelo SubBlog en el admin con su configuración
admin.site.register(SubBlog, SubBlogAdmin)

#se registra el modelo Imagen en el admin con su configuración
admin.site.register(Post, PostAdmin)

admin.site.register(Tag)

admin.site.register(Noticia, NoticiaAdmin)