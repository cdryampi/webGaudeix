from django.urls import path
from .views import RedSocialListView

app_name = 'redes_sociales'

urlpatterns = [
    path('redes-sociales/', RedSocialListView.as_view(), name='redes_sociales'),
]
