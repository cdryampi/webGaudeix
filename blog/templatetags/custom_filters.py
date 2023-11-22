from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def format_duration(duration):
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    
    if days > 0:
        if days == 1:
            days_string = 'dia'
        else:
            days_string = 'dies'
        parts.append(f"{days} {days_string}")
    
    if hours > 0:
        parts.append(f"{hours} hores")
    
    if minutes > 0:
        parts.append(f"{minutes} minuts")
    
    if seconds > 0:
        parts.append(f"{seconds} segons")
    
    return ' '.join(parts)



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)