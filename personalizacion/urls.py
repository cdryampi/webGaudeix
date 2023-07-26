from django.urls import path
from .views import ParallaxView
urlpatterns = [
    path('parallax/', ParallaxView.as_view(), name='parallax'),
]
