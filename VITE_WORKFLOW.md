# Vite + Tailwind CSS - Workflow

## 🚀 Quick Start

### Desarrollo (Pre-producción)

```bash
# Terminal 1: Vite dev server (HMR)
npm run dev

# Terminal 2: Django
.\venv\Scripts\activate
python manage.py runserver
```

**Importante:** En modo desarrollo, Vite sirve assets desde `http://localhost:5173` con Hot Module Replacement.

### Producción (DEBUG=False)

```bash
# 1. Build assets
npm run build

# 2. Collect static files
.\venv\Scripts\activate
python manage.py collectstatic --noinput

# 3. Run server
python manage.py runserver
```

---

## ⚠️ Bootstrap vs Tailwind

**PROBLEMA:** Bootstrap y Tailwind colisionan (ambos usan `.flex`, `.container`, etc.)

**SOLUCIÓN:** En templates que usen Tailwind, desactiva Bootstrap:

### Opción 1: Desactivar en template específico

```django
{# En tu-template.html #}
{% block extra_css %}
    <style>
        /* Desactivar Bootstrap solo en esta página */
        .bootstrap-override { all: revert; }
    </style>
{% endblock %}
```

### Opción 2: Comentar Bootstrap en base.html temporalmente

```django
{% compress css %}
    {# <link href="{% static 'core/bootstrap/css/bootstrap.min.css' %}"> #}
    ...otros CSS...
{% endcompress %}
```

### Opción 3: Orden de carga (actual)

```django
{# base.html - Tailwind carga DESPUÉS para tener prioridad #}
{% compress css %}
    <link href="bootstrap.min.css">  <!-- Bootstrap primero -->
{% endcompress %}

{% vite_asset 'js/main.js' %}  <!-- Tailwind después = prioridad -->
```

---

## 📁 Estructura de Archivos

```
static/
├── src/                    # Código fuente
│   ├── css/
│   │   └── main.css       # Tailwind + custom theme
│   └── js/
│       └── main.js        # Entry point (importa main.css)
│
├── dist/                   # Build output (npm run build)
│   ├── .vite/
│   │   └── manifest.json  # django-vite lo lee aquí
│   └── assets/
│       ├── main-[hash].css
│       └── main-[hash].js
│
└── [legacy files]         # Bootstrap, sample.css, etc.
```

---

## 🎨 Colores Gaudeix (Tokens)

```css
/* static/src/css/main.css */
@theme {
  --color-gaudeix-primary: #3ebfab; /* Turquesa */
  --color-gaudeix-secondary: #69920c; /* Verde */
  --color-gaudeix-accent: #e76500; /* Naranja */
}
```

**Uso en templates:**

```django
<div class="bg-gaudeix-primary text-white">
    Hola Cabrera!
</div>
```

---

## 🛠️ Comandos Útiles

```bash
# Instalar dependencias
npm install

# Desarrollo con HMR
npm run dev

# Build para producción
npm run build

# Ver qué genera Vite
ls static/dist/assets/

# Colectar estáticos
python manage.py collectstatic --noinput --clear

# Ver estáticos en producción
ls staticfiles/assets/
```

---

## 🔧 Configuración

### Django Settings

```python
# gaudeix/settings.py
INSTALLED_APPS = [
    'django_vite',  # Añadido
    ...
]

DJANGO_VITE = {
    'default': {
        'dev_mode': DEBUG,
        'dev_server_host': 'localhost',
        'dev_server_port': 5173,
        'manifest_path': BASE_DIR / 'static' / 'dist' / '.vite' / 'manifest.json',
    }
}
```

### Template Base

```django
{# core/templates/core/base.html #}
{% load django_vite %}

<head>
    {# CSS legacy comprimido #}
    {% compress css %}
        <link href="{% static 'fontawesomefree/css/all.min.css' %}">
        {# <link href="{% static 'core/bootstrap/css/bootstrap.min.css' %}"> #}
        <link href="{% static 'core/css/sample.css' %}">
    {% endcompress %}

    {# Tailwind CSS + JS moderno (carga último = prioridad) #}
    {% vite_asset 'js/main.js' %}
</head>
```

---

## 🐛 Troubleshooting

### ❌ "Tailwind no aplica estilos"

- ✅ Verifica que `npm run build` generó `main-[hash].css`
- ✅ Ejecuta `collectstatic` después del build
- ✅ Verifica que Bootstrap no esté sobrescribiendo (desactívalo)
- ✅ Hard refresh: `Ctrl + F5`

### ❌ "Error 404 en assets"

```bash
# En producción (DEBUG=False), SIEMPRE:
npm run build && python manage.py collectstatic --noinput
```

### ❌ "Clases custom no funcionan"

- ✅ Añádelas en `@layer utilities` en `main.css`
- ✅ Rebuild: `npm run build`

---

## 📚 Documentos de Referencia

- **Django-Vite:** https://github.com/MrBin99/django-vite
- **Tailwind CSS v4:** https://tailwindcss.com/docs
- **Vite:** https://vitejs.dev/guide/
- **Heroicons:** https://heroicons.com/

---

## ✅ Checklist Antes de Deploy

```bash
# 1. Build assets
npm run build

# 2. Verify build output
ls static/dist/assets/

# 3. Collect static
python manage.py collectstatic --noinput --clear

# 4. Verify collected files
ls staticfiles/assets/

# 5. Test con DEBUG=False
# En gaudeix/settings.py: DEBUG = False
python manage.py runserver

# 6. Test página 404
http://127.0.0.1:8000/preview-404/
```

---

**Última actualización:** 9 de octubre de 2025
