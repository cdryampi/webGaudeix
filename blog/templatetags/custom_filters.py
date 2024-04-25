from django import template
from django.utils.translation import gettext as _

register = template.Library()

@register.filter
def format_duration(duration):
    # Desglosa la duración en días, horas, minutos y segundos
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Crea una lista para los diferentes segmentos de tiempo
    parts = []

    # Añade días al resultado si es necesario
    if days > 0:
        days_string = _("dia") if days == 1 else _("dies")
        parts.append(f"{days} {days_string}")

    # Añade horas si es mayor que cero
    if hours > 0:
        if hours == 1:
            parts.append("1 " + _("hora"))  # Singular
        else:
            parts.append(f"{hours} " + _("hores"))  # Plural

    # Añade minutos si es mayor que cero
    if minutes > 0:
        if minutes == 1:
            parts.append("1 " + _("minut"))  # Singular
        else:
            parts.append(f"{minutes} " + _("minuts"))  # Plural

    # Añade segundos si es mayor que cero
    if seconds > 0:
        if seconds == 1:
            parts.append("1 " + _("segon"))  # Singular
        else:
            parts.append(f"{seconds} " + _("segons"))  # Plural

    # Une todas las partes en una sola cadena separada por espacios
    return ' '.join(parts)
