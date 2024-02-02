import csv
from agenda.models import Agenda

# Ruta al archivo CSV
csv_file_path = 'agenda_data.csv'

# Abre el archivo CSV y carga los datos en la base de datos
with open(csv_file_path, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        # Crea una instancia del modelo Agenda con los datos del CSV
        try:
            pk_a_buscar = row['pk']  # Reemplaza con la PK que deseas buscar
            agenda = Agenda.objects.get(pk=pk_a_buscar)
            # Ahora, puedes formatear el campo "description" a UTF-8
            description_utf8 = row['descripcion'].encode('utf-8')
            agenda.titulo = row['titulo'].encode('utf-8')
            agenda.descripcion = description_utf8
            agenda.descripcion_corta = row['descripcion_corta'].encode('utf-8')
            agenda.save()
            print(agenda)
        except Agenda.DoesNotExist:
            print("El registro con la PK especificada no existe en la base de datos.")

