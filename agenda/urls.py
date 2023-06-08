from django.urls import path

from .views import PDFView, AgendaDetailView



app_name = 'agenda'

urlpatterns = [
    path('calendario/', PDFView.as_view(), name='calendario_pdf'),
    path('<slug:slug>/', AgendaDetailView.as_view(), name='detalle_agenda'),

]
