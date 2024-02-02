import csv
from blog.models import Categoria  # Asegúrate de importar el modelo Agenda desde la ubicación correcta

# Obtén todos los objetos Agenda que deseas exportar
categorias = Categoria.objects.all()

# Especifica el nombre del archivo CSV de salida
archivo_csv = 'categoria_data.csv'

# Abre el archivo CSV en modo escritura
with open(archivo_csv, 'w', newline='') as csv_file:
    # Define el encabezado del archivo CSV
    fieldnames = ['pk', 'titulo', 'descripcion', 'subtitulo']
    
    # Crea el escritor CSV
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Escribe el encabezado en el archivo CSV
    writer.writeheader()
    
    # Itera sobre los objetos Agenda y escribe sus datos en el archivo CSV
    for categoria in categorias:
        writer.writerow({'pk': categoria.pk,'titulo': categoria.titulo, 'descripcion': categoria.descripcion,'subtitulo': categoria.subtitulo,})

print(f'Se ha generado el archivo CSV: {archivo_csv}')
