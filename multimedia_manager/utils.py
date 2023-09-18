import os
import uuid
import unicodedata
from unidecode import unidecode
from .errors import ExtensionInvalidaError, TamanioArchivoExcedidoError
from django.core.exceptions import ValidationError


ALLOWED_EXTENSIONS = {
    'imagen': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', 'webp'],
    'video': ['.mp4', '.avi', '.mov', '.mkv'],
    'fichero': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip']
}
MAX_TAMANIO_ARCHIVO = 33485760  # 30 MB





# Define una función para validar la calidad de la imagen
def validate_image_quality(image):
    if image.format != 'JPEG':
        raise ValidationError("El formato de la imagen debe ser JPEG.")
    
    # Verificar el tamaño de la imagen
    width, height = image.size
    if width < 800 or height < 600:
        raise ValidationError("El tamaño mínimo requerido para la imagen es de 800x600 píxeles.")
    
    # Verificar la calidad de la imagen (por ejemplo, si la calidad es menor a 80)
    # Esto dependerá de tus criterios específicos para la calidad de la imagen
    quality = image.info.get('quality')
    if quality and quality < 80:
        raise ValidationError("La calidad de la imagen debe ser de al menos 80.")



def utf8_friendly_filename(filename):
    # Translitera los caracteres unicode en caracteres ASCII
    safe_chars = unidecode(unicodedata.normalize('NFKD', filename)).encode('ASCII', 'ignore').decode('utf-8')
    return safe_chars.replace(" ", "_")

def generar_nombre_archivo(filename, tipo):
    nombre = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1].lower()

    # Translitera los caracteres unicode en caracteres ASCII
    safe_nombre = unidecode(unicodedata.normalize('NFKD', nombre)).encode('ASCII', 'ignore').decode('utf-8')

    if extension in ALLOWED_EXTENSIONS[tipo]:
        return os.path.join(tipo, f'{safe_nombre}{extension}')
    else:
        raise ExtensionInvalidaError('Extensión de archivo no permitida')

def validar_tamanio_archivo(archivo):
    tamanio_archivo = archivo.size
    if tamanio_archivo > MAX_TAMANIO_ARCHIVO:
        raise TamanioArchivoExcedidoError('El tamaño del archivo excede el límite permitido')

def upload_to_imagen(instance, filename):
    return generar_nombre_archivo(filename, tipo='imagen')


def upload_to_fichero(instance, filename):
    return generar_nombre_archivo(filename, tipo='fichero')

def upload_to_video(instance, filename):
    return generar_nombre_archivo(filename, tipo='video')
def delete_file(file):
    # Verificar si el archivo existe antes de eliminarlo
    if file and file.storage.exists(file.name):
        # Eliminar el archivo
        file.delete(save=False)
