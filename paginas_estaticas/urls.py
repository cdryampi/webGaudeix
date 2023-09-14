from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import PrivacitatView, AvisLegalView, PoliticaCookiesView, ContactoView, PuntInformacioView

app_name = 'paginas_estaticas'

urlpatterns = [
    path('privacitat/', PrivacitatView.as_view(), name='privacitat'),
    path('avis-legal/', AvisLegalView.as_view(), name='avis_legal'),
    path('politica-cookies/', PoliticaCookiesView.as_view(), name='politica_cookies'),
    path('contacte/', ContactoView.as_view(), name='contacto'),
    path('punt-informacio/', PuntInformacioView.as_view(), name='punt')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
