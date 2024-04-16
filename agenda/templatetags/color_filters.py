from django import template
import re

register = template.Library()

@register.filter(name='is_light')
def is_light(value):
    """
    Determina si un color (en formato hex) es lo suficientemente claro para que el texto sea negro.
    Devuelve True si es un color claro, de lo contrario False.
    """
    # Asegurar que el valor es una cadena
    if not isinstance(value, str):
        return False  # Asignar negro al texto si el color no es válido

    # Comprobar el formato de color hexadecimal
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value)
    if match:
        hex_color = value[1:]  # Remove the '#'
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])  # Convertir de formato corto a largo si es necesario
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        # Fórmula para calcular la luminancia y evaluar contra un umbral
        luminance = (0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]) / 255
        return luminance > 0.5  # Umbral de luminancia para texto negro sobre fondo claro
    return True  # Asignar texto blanco por defecto
