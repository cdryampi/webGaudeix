from collections import Counter
from .models import RedSocial

def obtener_color_mas_repetido():
    redes_sociales = RedSocial.objects.all()
    colores = [red_social.fondo for red_social in redes_sociales]
    contador = Counter(colores)
    color_mas_repetido = contador.most_common(1)[0][0] if contador else None
    return color_mas_repetido
