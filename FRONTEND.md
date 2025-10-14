# 🎨 Frontend Build System - Tailwind CSS v4 + Vite

Sistema de build moderno para el proyecto Gaudeix utilizando Tailwind CSS v4 y Vite.

## 📦 Instalación

Las dependencias ya están instaladas. Si necesitas reinstalarlas:

```bash
npm install
```

## 🚀 Comandos Disponibles

### Desarrollo

Inicia el servidor de desarrollo con hot-reload:

```bash
npm run dev
```

El servidor estará disponible en: `http://localhost:5173/static/`

### Producción

Construye los assets optimizados para producción:

```bash
npm run build
```

Los archivos compilados se generarán en `static/dist/` con:

- CSS minificado y optimizado
- JavaScript minificado
- Manifest file para integración con Django

### Watch Mode

Construye automáticamente cuando detecta cambios:

```bash
npm run watch
```

### Preview

Previsualiza el build de producción localmente:

```bash
npm run preview
```

## 📁 Estructura de Archivos

```
webGaudeix/
├── static/
│   ├── src/                      # Código fuente (tracked in git)
│   │   ├── css/
│   │   │   ├── main.css          # Entry point CSS con @theme
│   │   │   ├── components/       # Componentes Tailwind personalizados
│   │   │   └── utilities/        # Utilidades CSS personalizadas
│   │   ├── js/
│   │   │   ├── main.js           # Entry point JavaScript
│   │   │   ├── modules/          # Módulos JS (menu, carousel, etc.)
│   │   │   └── components/       # Componentes JS reutilizables
│   │   └── index.html            # HTML de prueba para desarrollo
│   ├── dist/                     # Build output (gitignored)
│   │   ├── .vite/
│   │   │   └── manifest.json     # Manifest para Django
│   │   └── assets/               # CSS/JS compilados con hash
│   └── [otros archivos estáticos existentes]
├── node_modules/                 # Dependencias npm (gitignored)
├── vite.config.js                # Configuración de Vite
└── package.json                  # Dependencias y scripts npm
```

## 🎨 Tema Gaudeix (Design Tokens)

El archivo `static/src/css/main.css` incluye los design tokens de Gaudeix:

### Colores Principales

```css
--color-gaudeix-primary: #3ebfab      /* Turquesa principal */
--color-gaudeix-secondary: #69920c    /* Verde oliva */
--color-gaudeix-accent: #e76500       /* Naranja acento */
```

### Uso en HTML

```html
<!-- Background turquesa -->
<div class="bg-gaudeix-primary">...</div>

<!-- Texto verde oliva con hover -->
<a class="text-gaudeix-secondary hover:text-gaudeix-secondary-dark">...</a>

<!-- Botón con color acento -->
<button class="bg-gaudeix-accent text-white">...</button>
```

### Colores Disponibles

- `gaudeix-primary` / `gaudeix-primary-dark` / `gaudeix-primary-light`
- `gaudeix-secondary` / `gaudeix-secondary-dark` / `gaudeix-secondary-light`
- `gaudeix-accent`
- `gaudeix-warning` (#ffc107)
- `gaudeix-info` (#17a2b8)
- `gaudeix-ocean` (#007bff)
- `gaudeix-dark` (#2c3e50)

## 🔧 Configuración de Vite

El archivo `vite.config.js` está configurado para:

- **Root**: `./static/src` - Directorio de origen
- **Base**: `/static/` - URL base para assets
- **Output**: `./static/dist` - Directorio de salida
- **Entry points**: `main.js` y `main.css`
- **Port**: 5173
- **Manifest**: Generado automáticamente para Django

## 📚 Integración con Django

### Opción 1: django-vite (Recomendado)

Instalar el paquete:

```bash
pip install django-vite
```

Configurar en `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'django_vite',
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

Usar en templates:

```django
{% load django_vite %}

<!DOCTYPE html>
<html>
<head>
    {% vite_asset 'css/main.css' %}
</head>
<body>
    {% vite_asset 'js/main.js' %}
</body>
</html>
```

### Opción 2: Manual

En desarrollo, el servidor de Vite debe estar corriendo (`npm run dev`).

En producción, ejecutar `npm run build` antes de `python manage.py collectstatic`.

## ✅ FASE 1 Completada

### Lo que se ha instalado:

- ✅ Node.js inicializado (`package.json`)
- ✅ Tailwind CSS v4.1.14 instalado
- ✅ Plugin `@tailwindcss/vite` v4.1.14
- ✅ Vite v7.1.9 configurado
- ✅ Estructura de directorios creada
- ✅ Archivos de entrada (`main.css`, `main.js`)
- ✅ Tema Gaudeix con custom colors
- ✅ Scripts npm configurados
- ✅ Build system funcionando ✅

### Archivos generados:

```
📦 Output del build:
├── static/dist/.vite/manifest.json   (0.28 kB)
├── static/dist/assets/styles-c9Nk9bHI.css   (10.29 kB → 2.86 kB gzipped)
└── static/dist/assets/main-DgrGUbHE.js      (0.06 kB)
```

### Próximos pasos:

1. **FASE 2**: Exportar design tokens completos desde Google Stitch
2. **Subtarea #25**: Migrar `core/templates/core/base.html` a Tailwind
3. **Subtarea #26**: Migrar navegación (header)
4. **Subtarea #27**: Migrar footer

## 🐛 Troubleshooting

### El servidor no inicia

Verifica que el puerto 5173 esté libre:

```bash
npm run dev
```

### Build falla

Limpia la caché y reinstala:

```bash
rm -rf node_modules
rm package-lock.json
npm install
npm run build
```

### CSS no se aplica

1. Verifica que Vite esté corriendo en desarrollo
2. En producción, asegúrate de haber ejecutado `npm run build`
3. Revisa que las rutas en los templates sean correctas

## 📝 Notas

- **No commitear**: `node_modules/`, `static/dist/` (están en .gitignore)
- **Sí commitear**: Todo en `static/src/`, `vite.config.js`, `package.json`
- Los archivos en `static/dist/` se generan automáticamente en cada build
- El manifest.json es necesario para la integración con Django

---

**Versión**: 1.0.0  
**Issue**: #3 - Setup Tailwind CSS y Sistema de Build con Vite  
**Última actualización**: Octubre 2025
