from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from legal.views import PrivacitatView, AvisLegalView, PoliticaCookiesView

app_name = 'legal'

urlpatterns = [
    path('privacitat/', PrivacitatView.as_view(), name='privacitat'),
    path('avis-legal/', AvisLegalView.as_view(), name='avis_legal'),
    path('politica-cookies/', PoliticaCookiesView.as_view(), name='politica_cookies'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
