from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'legal'

urlpatterns = [
    path('privacitat/', views.privacitat, name='privacitat'),
    path('avis-legal/', views.avis_legal, name='avis_legal'),
    path('politica-cookies/', views.politica_cookies, name='politica_cookies'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
