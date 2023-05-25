from django.urls import path
from .views import TopbarView

urlpatterns = [
    path('topbar/', TopbarView.as_view(), name='topbar'),
]
