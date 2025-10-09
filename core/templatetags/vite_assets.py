"""
Templatetags para cargar assets de Vite/Tailwind en Django
"""
import json
import os
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

# Cache del manifest para no leerlo en cada request
_manifest_cache = None


def get_manifest():
    """Lee el manifest.json generado por Vite"""
    global _manifest_cache
    
    if _manifest_cache is not None and not settings.DEBUG:
        return _manifest_cache
    
    manifest_path = os.path.join(
        settings.BASE_DIR, 
        'static', 
        'dist', 
        '.vite', 
        'manifest.json'
    )
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            _manifest_cache = json.load(f)
            return _manifest_cache
    except FileNotFoundError:
        # Si no existe el manifest, estamos en desarrollo
        # Devuelve rutas directas sin hash
        return {
            'css/main.css': {
                'file': 'assets/main.css',
                'isEntry': True
            },
            'js/main.js': {
                'file': 'assets/main.js',
                'isEntry': True
            }
        }


@register.simple_tag
def vite_css(entry='css/main.css'):
    """
    Genera la etiqueta <link> para cargar CSS de Vite
    
    Uso en template:
        {% load vite_assets %}
        {% vite_css 'css/main.css' %}
    """
    manifest = get_manifest()
    
    if entry in manifest:
        css_file = manifest[entry]['file']
        css_url = f"{settings.STATIC_URL}{css_file}"
        return mark_safe(f'<link rel="stylesheet" href="{css_url}">')
    
    # Fallback para desarrollo
    return mark_safe(f'<link rel="stylesheet" href="{settings.STATIC_URL}{entry}">')


@register.simple_tag
def vite_js(entry='js/main.js'):
    """
    Genera la etiqueta <script> para cargar JavaScript de Vite
    
    Uso en template:
        {% load vite_assets %}
        {% vite_js 'js/main.js' %}
    """
    manifest = get_manifest()
    
    if entry in manifest:
        js_file = manifest[entry]['file']
        js_url = f"{settings.STATIC_URL}{js_file}"
        return mark_safe(f'<script type="module" src="{js_url}"></script>')
    
    # Fallback para desarrollo
    return mark_safe(f'<script type="module" src="{settings.STATIC_URL}{entry}"></script>')


@register.simple_tag
def vite_dev_server():
    """
    Incluye el cliente de HMR de Vite en desarrollo
    
    Uso en template:
        {% if DEBUG %}
            {% vite_dev_server %}
        {% endif %}
    """
    if settings.DEBUG:
        return mark_safe(
            '<script type="module" src="http://localhost:5173/@vite/client"></script>'
        )
    return ''
