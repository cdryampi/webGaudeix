import csv
from blog.models import Categoria

# Ruta al archivo CSV
csv_file_path = 'categorias_data.csv'

# Abre el archivo CSV y asegura la codificación UTF-8
with open(csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        # Crea o actualiza la instancia del modelo Categoria con los datos del CSV
        try:
            pk_a_buscar = row['pk']  # Utiliza la PK para buscar el registro existente
            categoria = Categoria.objects.get(pk=pk_a_buscar)

            # Asigna los valores directamente sin necesidad de codificarlos
            categoria.titulo_ca = row['titulo']
            categoria.titulo_es = row['titulo_spanish']
            categoria.titulo_en = row['titulo_english']

            categoria.descripcion_ca = row['descripcion']
            categoria.descripcion_es = row['descripcion_spanish']
            categoria.descripcion_en = row['descripcion_english']

            categoria.subtitulo_ca = row['subtitulo']
            categoria.subtitulo_es = row['subtitulo_spanish']
            categoria.subtitulo_en = row['subtitulo_english']
            
            categoria.save()
            print(f"Categoria actualizada: {categoria}")
        except Categoria.DoesNotExist:
            print("El registro con la PK especificada no existe en la base de datos.")
