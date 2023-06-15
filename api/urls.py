from django.urls import path
from .views import TeenvioView
app_name = 'api'
urlpatterns = [
        path('newsletter/', TeenvioView.as_view(), name='newsletter'),
]
