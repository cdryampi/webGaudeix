from django.urls import path

from .views import PDFView, AgendaDetailView, VisitaGuiadaView, RutaView, ICSAgenda, DescargarPlaylist, GenerarRSS, AlojamientoView, RestauranteView, TurismeSostenibleView



app_name = 'agenda'

urlpatterns = [
    path('calendario/', PDFView.as_view(), name= 'calendario_pdf'),
    path('ics/', ICSAgenda.as_view(), name= 'agenda_ics'),
    path('descargar-playlist/', DescargarPlaylist.as_view(), name= 'descargar-audio'),
    path('visites-guiades/<slug:slug>/', VisitaGuiadaView.as_view(), name= 'visites-guiades'),
    path('ruta/<slug:slug>/', RutaView.as_view(), name= 'ruta'),
    path('descargar-playlist-rss/',GenerarRSS.as_view(), name= 'descargar-audio-rss'),
    path('allotjament/<slug:slug>/', AlojamientoView.as_view(), name= 'allotjament'),
    path('restaurant/<slug:slug>/', RestauranteView.as_view(), name="restaurant"),
    path('sostenibilitat/<slug:slug>/', TurismeSostenibleView.as_view(), name="turisme_sostenible"),
    path('<slug:slug>/', AgendaDetailView.as_view(), name= 'detalle_agenda'),
]
