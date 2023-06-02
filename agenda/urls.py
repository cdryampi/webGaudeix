from django.urls import path
from .views import AgendaListView
from .views import PDFView



app_name = 'agenda'

urlpatterns = [
    path('', AgendaListView.as_view(), name='agenda'),
    path('calendario/', PDFView.as_view(), name='calendario_pdf'),

]
