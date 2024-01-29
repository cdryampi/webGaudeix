from django.urls import path

from .views import PDFView, AgendaDetailView, VisitaGuiadaView, RutaView, ICSAgenda, DescargarPlaylist



app_name = 'agenda'

urlpatterns = [
    path('calendario/', PDFView.as_view(), name='calendario_pdf'),
    path('ics/', ICSAgenda.as_view(), name='agenda_ics'),
    path('descargar-playlist/', DescargarPlaylist.as_view(), name='descargar-audio'),
    path('visites-guiades/<slug:slug>', VisitaGuiadaView.as_view(), name='visites-guiades'),
    path('ruta/<slug:slug>/', RutaView.as_view(), name='ruta'),
    path('<slug:slug>/', AgendaDetailView.as_view(), name='detalle_agenda'),

]
