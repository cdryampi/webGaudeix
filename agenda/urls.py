from django.urls import path

from .views import PDFView, AgendaDetailView, VisitaGuiadaView, RutaView



app_name = 'agenda'

urlpatterns = [
    path('calendario/', PDFView.as_view(), name='calendario_pdf'),
    path('<slug:slug>/', AgendaDetailView.as_view(), name='detalle_agenda'),
    path('visites-guiades/<slug:slug>', VisitaGuiadaView.as_view(), name='visites-guiades'),
    path('ruta/<slug:slug>/', RutaView.as_view(), name='ruta')
]
