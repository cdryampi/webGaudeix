import os
import uuid
from .errors import ExtensionInvalidaError, TamanioArchivoExcedidoError


ALLOWED_EXTENSIONS = {
    'imagen': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'video': ['.mp4', '.avi', '.mov', '.mkv'],
    'fichero': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
}
MAX_TAMANIO_ARCHIVO = 10485760  # 10 MB


def generar_nombre_archivo(filename, tipo):
    nombre = os.path.splitext(filename)[0].lower()
    extension = os.path.splitext(filename)[1].lower()
    if extension in ALLOWED_EXTENSIONS[tipo]:
        return os.path.join(tipo, f'{nombre}{extension}')
    else:
        raise ExtensionInvalidaError('Extensión de archivo no permitida')

def validar_tamanio_archivo(archivo):
    tamanio_archivo = archivo.size
    if tamanio_archivo > MAX_TAMANIO_ARCHIVO:
        raise TamanioArchivoExcedidoError('El tamaño del archivo excede el límite permitido')

def upload_to_imagen(instance, filename):
    return generar_nombre_archivo(filename, tipo='imagen')



def delete_file(file):
    # Verificar si el archivo existe antes de eliminarlo
    if file and file.storage.exists(file.name):
        # Eliminar el archivo
        file.delete(save=False)
