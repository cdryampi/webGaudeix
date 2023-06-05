from django.urls import path
from .views import ParallaxView, PortadaVideoAPIView
urlpatterns = [
    path('parallax/', ParallaxView.as_view(), name='parallax'),
    path('api/portada-video/', PortadaVideoAPIView.as_view(), name='portada-video-api'),

]
