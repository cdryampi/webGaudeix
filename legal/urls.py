from django.urls import path
from . import views

app_name = 'legal'

urlpatterns = [
    path('privacitat/', views.privacitat, name='privacitat'),
    path('avis-legal/', views.avis_legal, name='avis_legal'),
    path('politica-cookies/', views.politica_cookies, name='politica_cookies'),
]
