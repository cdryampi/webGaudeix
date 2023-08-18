from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from core.utils import refresh_cache
from ..models import Noticia
from ..utils import sincronizar_noticias



class NoticiaAdmin(admin.ModelAdmin):
    actions = ['sincronizar_feed','refresh_cache']

    def sincronizar_feed(self, request, queryset):
        if queryset.exists():
            try:
                sincronizar_noticias()
                self.message_user(request, "El feed de notícies s'ha sincronitzat correctament.")
            except Exception as e:
                messages.error(request, f"Error en la sincronització del feed de notícies: {str(e)}")
        else:
            self.message_user(request, "No s'han seleccionat elements per sincronitzar.", level='warning')

    def changelist_view(self, request, extra_context=None):
        messages.info(request, "Sincronitzem el feed de les notícies dels RRSS de l'Ajuntament de Cabrera de Mar. Quan es sincronitza, assegura't de revisar que les noves notícies creades estiguin a la categoria 'Notícia'. Per poder realitzar l'acció, selecciona tots els elements al quadre de selecció 'Notícia' i després selecciona l'opció 'Sincronitzar feed de notícies' al desplegable.")
        return super().changelist_view(request, extra_context=extra_context)

    sincronizar_feed.short_description = "Sincronitzar feed de notícies"


    def refresh_cache(self, request, queryset):
        refresh_cache(request)
        self.message_user(request, "La memòria cau de la pàgina d'inici s'ha refrescat amb èxit.")

    refresh_cache.short_description = "Refrescar Caché"