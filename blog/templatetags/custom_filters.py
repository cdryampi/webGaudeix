from django import template
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

register = template.Library()

@register.filter
def format_duration(duration):
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    
    if days > 0:
        days_string = _("dia") if days == 1 else _("dies")
        parts.append(f"{days} {days_string}")
    
    if hours > 0:
        parts.append(f"{hours} " + _("hores"))
    
    if minutes > 0:
        parts.append(f"{minutes} " + _("minuts"))
    
    if seconds > 0:
        parts.append(f"{seconds} " + _("segons"))
    
    return ' '.join(parts)
