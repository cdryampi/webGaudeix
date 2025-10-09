# Gestión de Archivos Estáticos en Django

## 📁 Estructura de Archivos Estáticos

### Desarrollo (DEBUG=True)

Cuando `DEBUG=True`, Django sirve archivos estáticos directamente desde `STATICFILES_DIRS`:

```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/static'),       # Bootstrap, jQuery, CSS legacy
    os.path.join(BASE_DIR, 'static/dist'),       # Vite/Tailwind build output
]
```

**URLs servidas:**
- `/static/core/...` → Archivos de `core/static/`
- `/static/assets/...` → Archivos de `static/dist/assets/`

### Producción (DEBUG=False)

Cuando `DEBUG=False`, Django **NO** sirve archivos estáticos automáticamente. Debes:

1. **Compilar assets con Vite:**
   ```bash
   npm run build
   ```
   
2. **Recopilar todos los estáticos:**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Configurar servidor web** (Nginx, Apache, Whitenoise) para servir desde `STATIC_ROOT`

---

## ⚙️ Configuración

### settings.py

```python
# URL base para archivos estáticos
STATIC_URL = '/static/'

# Directorios de origen (DEBUG=True)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/static'),
    os.path.join(BASE_DIR, 'static/dist'),  # Vite output
]

# Directorio de destino (DEBUG=False)
# IMPORTANTE: Debe ser DIFERENTE de STATICFILES_DIRS
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### .gitignore

```gitignore
# Ignorar archivos generados
/static/dist/         # Output de Vite (npm run build)
/staticfiles/         # Archivos recopilados (collectstatic)
node_modules/
```

---

## 🔄 Workflow de Desarrollo

### 1. Desarrollo con Hot Reload (Vite Dev Server)

Si quieres **hot reload** en desarrollo:

```bash
# Terminal 1: Vite dev server
npm run dev

# Terminal 2: Django dev server
python manage.py runserver
```

Modifica `base.html` para usar el dev server:
```django
{% if debug %}
    {# Desarrollo: Vite dev server #}
    <script type="module" src="http://localhost:5173/@vite/client"></script>
    <link rel="stylesheet" href="http://localhost:5173/css/main.css">
{% else %}
    {# Producción: Assets compilados #}
    {% load vite_assets %}
    {% vite_css 'css/main.css' %}
    {% vite_js 'js/main.js' %}
{% endif %}
```

### 2. Desarrollo sin Hot Reload (Assets Compilados)

Si prefieres trabajar con **assets compilados** (como ahora):

```bash
# 1. Compilar assets cuando cambies Tailwind
npm run build

# 2. Django sirve desde static/dist/
python manage.py runserver

# Los archivos se sirven directamente gracias a STATICFILES_DIRS
```

### 3. Producción (DEBUG=False)

```bash
# 1. Compilar assets para producción
npm run build

# 2. Recopilar todos los estáticos
python manage.py collectstatic --noinput

# 3. Configurar servidor web para servir staticfiles/
# Ejemplo con Whitenoise:
pip install whitenoise
# Añadir a MIDDLEWARE en settings.py
```

---

## 🛠️ Comandos Útiles

### Compilar Assets de Tailwind CSS

```bash
# Desarrollo (watch mode)
npm run dev

# Producción (minificado)
npm run build
```

**Output:**
- `static/dist/.vite/manifest.json` - Mapa de assets
- `static/dist/assets/styles-[hash].css` - Tailwind CSS compilado
- `static/dist/assets/main-[hash].js` - JavaScript bundled

### Recopilar Archivos Estáticos

```bash
# Recopilar todos los archivos
python manage.py collectstatic

# Sin confirmación (CI/CD)
python manage.py collectstatic --noinput

# Limpiar y recopilar
python manage.py collectstatic --clear --noinput
```

### Verificar Template Tags

```bash
# Reiniciar servidor Django después de crear template tags
Ctrl+C
python manage.py runserver
```

---

## 📊 Flujo de Archivos

### Desarrollo (DEBUG=True)

```
static/src/css/main.css
     ↓ (npm run build)
static/dist/assets/styles-c9Nk9bHI.css
     ↓ (STATICFILES_DIRS)
http://127.0.0.1:8000/static/assets/styles-c9Nk9bHI.css
     ↓ ({% vite_css %})
<link href="/static/assets/styles-c9Nk9bHI.css">
```

### Producción (DEBUG=False)

```
static/src/css/main.css
     ↓ (npm run build)
static/dist/assets/styles-c9Nk9bHI.css
     ↓ (collectstatic)
staticfiles/assets/styles-c9Nk9bHI.css
     ↓ (Nginx/Whitenoise)
https://gaudeix.cat/static/assets/styles-c9Nk9bHI.css
     ↓ ({% vite_css %})
<link href="/static/assets/styles-c9Nk9bHI.css">
```

---

## 🐛 Troubleshooting

### Problema: CSS de Tailwind no carga en DEBUG=False

**Causa:** No has ejecutado `collectstatic` después de `npm run build`

**Solución:**
```bash
npm run build
python manage.py collectstatic --noinput
```

### Problema: "Found another file with the destination path"

**Causa:** Archivos duplicados en `STATICFILES_DIRS` (normal si tienes múltiples apps)

**Solución:** Ignorar warnings o usar `--clear` para limpiar antes:
```bash
python manage.py collectstatic --clear --noinput
```

### Problema: 404 en archivos estáticos en producción

**Causa:** Servidor web no está configurado para servir `STATIC_ROOT`

**Solución con Whitenoise:**
```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← Añadir aquí
    # ... resto de middleware
]

# Opcional: Comprimir y cachear assets
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Problema: Cambios en Tailwind CSS no se reflejan

**Causa:** Assets no recompilados

**Solución:**
```bash
# 1. Recompilar Vite
npm run build

# 2. Si DEBUG=False, recopilar estáticos
python manage.py collectstatic --noinput

# 3. Reiniciar servidor Django
Ctrl+C
python manage.py runserver
```

---

## 📦 Estructura Final

```
webGaudeix/
├── static/
│   ├── src/                    # Código fuente (Tailwind, JS)
│   │   ├── css/main.css
│   │   ├── js/main.js
│   │   └── index.html
│   └── dist/                   # Output de Vite (generado)
│       ├── .vite/
│       │   └── manifest.json
│       └── assets/
│           ├── styles-[hash].css
│           └── main-[hash].js
├── core/static/                # Assets legacy (Bootstrap, jQuery)
│   ├── bootstrap/
│   ├── css/
│   ├── js/
│   └── ...
├── staticfiles/                # Recopilación para producción (generado)
│   ├── admin/
│   ├── assets/                 # ← Tailwind CSS aquí
│   ├── core/
│   └── ...
├── core/templatetags/
│   └── vite_assets.py          # Template tags personalizados
└── gaudeix/
    └── settings.py             # Configuración estática
```

---

## ✅ Checklist Pre-Deploy

- [ ] Compilar assets: `npm run build`
- [ ] Recopilar estáticos: `python manage.py collectstatic --noinput`
- [ ] Verificar `STATIC_ROOT` configurado correctamente
- [ ] Configurar servidor web (Nginx/Whitenoise) para servir `staticfiles/`
- [ ] Probar con `DEBUG=False` localmente
- [ ] Verificar que CSS/JS cargan en navegador (DevTools Network)
- [ ] Confirmar hashes en manifest: `static/dist/.vite/manifest.json`

---

## 📚 Referencias

- [Django Static Files](https://docs.djangoproject.com/en/4.2/howto/static-files/)
- [Vite Build](https://vitejs.dev/guide/build.html)
- [Whitenoise Django](http://whitenoise.evans.io/en/stable/)
- [Tailwind CSS v4](https://tailwindcss.com/docs/v4-beta)
