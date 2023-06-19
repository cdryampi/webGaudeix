from django.contrib import admin
from django.contrib import messages
from ..models import Noticia
from ..utils import sincronizar_noticias



class NoticiaAdmin(admin.ModelAdmin):
    actions = ['sincronizar_feed']


    def sincronizar_feed(self, request, queryset):
        if queryset.exists():
            try:
                sincronizar_noticias()
                self.message_user(request, "El feed de noticias se ha sincronizado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al sincronizar el feed de noticias: {str(e)}")
        else:
            self.message_user(request, "No se han seleccionado elementos para sincronizar.", level='warning')

    sincronizar_feed.short_description = "Sincronizar feed de noticias"
    sincronizar_feed.short_description = "Sincronizar feed de noticias"


