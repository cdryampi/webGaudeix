from django.urls import include,path
from .views import CompaDescubreView

app_name = 'compra_y_descubre'
urlpatterns = [
    # Otras URLs de la aplicación "core"
    # ...
    path('<slug:slug>', CompaDescubreView.as_view(), name='compra_y_descubre'),
]
