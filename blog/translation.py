from modeltranslation.translator import translator, TranslationOptions, register
from .models import Post, SubBlog, Categoria, SubCategoria # Asegúrate de importar tu modelo

# Define las opciones de traducción para el modelo Post
@register(SubBlog)
class SubBlogTranslationOptions(TranslationOptions):
    fields = ('titulo', 'contenido',)

@register(Categoria)
class CategoriaTranslationOptions(TranslationOptions):
    fields = ('titulo', 'subtitulo', 'descripcion')
    
@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('titulo', 'descripcion',)  # Lista de campos que deseas traducir

@register(SubCategoria)
class TranslationOptions(TranslationOptions):
    fields = ('titulo', 'subtitulo', 'descripcion',)