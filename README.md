# Gaudeix CMS: Sistema de Gestión de Contenidos para Municipios

## Descripción

El proyecto Gaudeix es un sistema de gestión de contenido (CMS) desarrollado específicamente para mejorar la comunicación y el acceso a la información en municipios. Construido sobre Django 4.2.1, este CMS robusto y flexible ofrece una solución integral "todo en uno" para la gestión de contenido web, la promoción del turismo local, y el soporte al comercio y eventos en el municipio.

## Características Destacadas

- **Agenda Integrada**: Permite a los usuarios acceder y descargar en formato PDF un calendario de eventos locales, mejorando significativamente la participación comunitaria.

- **Soporte Multilingüe**: Asegura que el contenido del sitio web sea accesible para una audiencia global, fomentando el turismo y la inclusividad cultural.

- **Generador de Páginas Especiales para Eventos**: Con funcionalidades avanzadas como efectos parallax, galerías de imágenes en mosaico, y cuentas atrás para eventos futuros, ofreciendo una rica experiencia de usuario.

- **Aplicación de Rutas Autoguiadas**: Incluye mapas interactivos con marcas personalizadas, detalles de puntos de interés, y listas de reproducción de audio para enriquecer la experiencia turística.

- **Directorio de Negocios Locales**: Promueve el comercio local mediante un sistema de listado y filtros para hoteles, restaurantes y otros negocios, con páginas de aterrizaje personalizadas.

- **Integración de APIs Externas**: Extiende la funcionalidad del CMS integrando servicios externos para mantener el sitio actualizado y enriquecido.

- **Gestión Responsive de Imágenes**: A través de `imagekit.processors`, optimiza la entrega de imágenes para todos los dispositivos, mejorando la velocidad de carga y la experiencia del usuario.

- **Panel de Administración Personalizado de Django**: Facilita la gestión del contenido a los administradores con una interfaz amigable y documentación integrada para cada componente.

## Tecnologías Utilizadas

- Django 5.2.7
- Python 3.x
- **Vite 7.1.9** - Build tool moderno con HMR
- **Tailwind CSS 4.1.14** - Framework CSS utility-first
- HTML, CSS, JavaScript
- ImageKit
- APIs externas
- CKEditor para edición de texto enriquecido
- Bootstrap 4 (legacy, en proceso de migración a Tailwind)

## Inicio Rápido

### Instalación

1. Clone el repositorio:

   ```bash
   git clone https://github.com/cdryampi/webGaudeix/
   cd webGaudeix
   ```

2. Cree y active el entorno virtual:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   ```

3. Instale dependencias Python:

   ```bash
   pip install -r requirements.txt
   ```

4. Instale dependencias Node.js:

   ```bash
   npm install
   ```

5. Realice las migraciones:
   ```bash
   python manage.py migrate
   ```

### Desarrollo (con Vite HMR)

```bash
# Terminal 1: Vite dev server
npm run dev

# Terminal 2: Django server
.\venv\Scripts\activate
python manage.py runserver
```

Visite `http://localhost:8000` en su navegador.

### Producción

```bash
# Build assets
npm run build

# Collect static files
python manage.py collectstatic --noinput

# Run server
python manage.py runserver
```

## 📚 Documentación

- **[VITE_WORKFLOW.md](./VITE_WORKFLOW.md)** - Guía completa de Vite + Tailwind CSS
- **[AGENTS.md](./AGENTS.md)** - Guías para desarrollo con LLMs

## 🎨 Sistema de Diseño

El proyecto utiliza Tailwind CSS 4 con tokens personalizados Gaudeix:

- `--color-gaudeix-primary`: #3ebfab (Turquesa)
- `--color-gaudeix-secondary`: #69920c (Verde)
- `--color-gaudeix-accent`: #e76500 (Naranja)

Ver `static/src/css/main.css` para más detalles.
