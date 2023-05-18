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
    extension = os.path.splitext(filename)[1].lower()
    if extension in ALLOWED_EXTENSIONS[tipo]:
        nombre_aleatorio = uuid.uuid4().hex
        return os.path.join('media', tipo, f'{nombre_aleatorio}{extension}')
    else:
        raise ExtensionInvalidaError('Extensión de archivo no permitida')

def validar_tamanio_archivo(archivo):
    tamanio_archivo = archivo.size
    if tamanio_archivo > MAX_TAMANIO_ARCHIVO:
        raise TamanioArchivoExcedidoError('El tamaño del archivo excede el límite permitido')

def upload_to_imagen(instance, filename):
    return generar_nombre_archivo(filename, tipo='imagen')