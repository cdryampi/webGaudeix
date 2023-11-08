import uuid
from django.core.cache import caches
from django_user_agents.utils import get_user_agent
from django.core.cache import cache
from django.http import HttpResponse
import qrcode
from PIL import Image
from io import BytesIO




def generate_qr_code(url, color="#000000"):
    # Crear un objeto QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Agregar la URL al código QR
    qr.add_data(url)
    qr.make(fit=True)

    # Crear una imagen QR
    qr_img = qr.make_image(fill_color=color, back_color="#FFFFFF")

    # Guardar la imagen QR en un archivo temporal
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    return buffer.getvalue()











def generate_short_slug():
    # Genera un UUID y toma los primeros 8 caracteres de la representación hexadecimal
    return str(uuid.uuid4().hex)[:5]





def generate_cache_key(request):
    user_agent = request.META.get('HTTP_USER_AGENT')
    if user_agent:
        safe_user_agent = user_agent.replace(" ", "_").replace(":", "_")
    else:
        safe_user_agent = "unknown"
    cache_key = f"{request.path}:{safe_user_agent}"
    return cache_key



def refresh_cache(request):
    # Eliminar la clave de caché para refrescarla
    cache_key = generate_cache_key(request)
    cache.delete(cache_key)
    return HttpResponse("Caché refrescada exitosamente.")



