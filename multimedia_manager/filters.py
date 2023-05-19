from dal.autocomplete import Select2ListView
from .models import Imagen

# class ImagenAutocomplete(Select2ListView):
#     def create(self, text):
#         # Obtener la instancia de Imagen existente según el título seleccionado
#         try:
#             imagen = Imagen.objects.get(titulo=text)
#         except Imagen.DoesNotExist:
#             imagen = None
        
#         return imagen

#     def get_list(self):
#         tipo = 'imagen'  # Reemplaza 'imagen' con el tipo deseado
#         modelo = self.model  # Obtiene el modelo de la instancia actual
#         return Imagen.objects.filter(tipo=tipo, modelo=modelo).values_list('titulo', flat=True)


#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return Imagen.objects.none()
#         qs = Imagen.objects.images()  # Filtrar solo imágenes
#         if self.q:
#             qs = qs.filter(titulo__istartswith=self.q)
#         return qs
    