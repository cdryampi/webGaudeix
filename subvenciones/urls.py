from django.urls import path
from .views import SubvencionsListView, SubvencionListView

app_name= 'subvencions'

urlpatterns = [
        path('', SubvencionsListView.as_view(), name='subvencions'),
        path('<slug:slug>', SubvencionListView.as_view(), name='subvencio')
]
