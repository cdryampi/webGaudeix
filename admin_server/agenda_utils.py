import csv
from agenda.models import Agenda  # Asegúrate de importar el modelo Agenda desde la ubicación correcta

# Obtén todos los objetos Agenda que deseas exportar
agendas = Agenda.objects.all()

# Especifica el nombre del archivo CSV de salida
archivo_csv = 'agenda_data.csv'

# Abre el archivo CSV en modo escritura
with open(archivo_csv, 'w', newline='') as csv_file:
    # Define el encabezado del archivo CSV
    fieldnames = ['pk','titulo', 'descripcion_corta', 'descripcion']
    
    # Crea el escritor CSV
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Escribe el encabezado en el archivo CSV
    writer.writeheader()
    
    # Itera sobre los objetos Agenda y escribe sus datos en el archivo CSV
    for agenda in agendas:
        writer.writerow({'pk': agenda.pk,'titulo': agenda.titulo,'descripcion_corta': agenda.descripcion_corta,'descripcion': agenda.descripcion,})

print(f'Se ha generado el archivo CSV: {archivo_csv}')
