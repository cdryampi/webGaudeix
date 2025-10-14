# Header Template Structure

## Estructura Modular

El header ha sido dividido en componentes pequeños y manejables para facilitar el mantenimiento y corrección de errores.

## Archivos

### `header.html` (Principal)
Archivo principal que orquesta todos los componentes. Contiene solo 59 líneas.

### Carpeta `partials/`

#### `_logo.html`
- Sección del logo principal
- Logo del evento especial (si existe)
- Logo de Gaudeix Cabrera de Mar

#### `_mobile_button.html`
- Botón hamburguesa para menú móvil
- Integración con Flowbite collapse

#### `_nav_externo.html`
- Enlaces externos
- Soporte para estilos personalizados y colores

#### `_nav_post.html`
- Enlaces a posts individuales

#### `_nav_categoria.html`
- Categorías simples (sin subcategorías)
- Categorías con dropdown de subcategorías
- Botón "Veure més"

#### `_nav_subblog.html`
- SubBlogs con categorías (multinivel)
- Nivel 2: Categorías del subblog
- Nivel 3: Subcategorías con positioning a la derecha
- Soporte completo para dropdowns anidados

#### `_nav_otros.html`
- Contacto
- Eventos especiales (estilo destacado)
- Punt d'Informació
- Compra y Descubre

#### `_language_selector.html`
- Selector de idioma con banderas
- Formularios para cambio de idioma
- Soporte para catalán y otros idiomas

## Ventajas de esta estructura

1. **Fácil mantenimiento**: Cada componente es independiente
2. **Corrección de errores simplificada**: Los errores están aislados en archivos pequeños
3. **Reutilización**: Los partials pueden usarse en otros contextos
4. **Legibilidad**: El archivo principal es muy claro
5. **Testing**: Cada componente puede probarse de forma independiente

## Cómo editar

Para modificar un elemento específico:

1. Identifica el tipo de elemento (logo, categoría, subblog, etc.)
2. Abre el archivo partial correspondiente en `partials/`
3. Realiza los cambios necesarios
4. Los cambios se reflejarán automáticamente en el header principal

## Backup

El archivo original se encuentra en `header_backup.html` por si necesitas revertir los cambios.
