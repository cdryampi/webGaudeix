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

- Django 4.2.1
- Python
- HTML, CSS, JS
- ImageKit
- APIs externas
- CKEditor para edición de texto enriquecido
- Bootstrap 4 para diseño responsive

## Inicio Rápido

Para comenzar a usar Gaudeix CMS, sigue estos pasos:

1. Clone el repositorio:
   ```
   git clone [https://github.com/cdryampi/webGaudeix/]
   ```
2. Instale las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Realice las migraciones necesarias:
   ```
   python manage.py migrate
   ```
4. Inicie el servidor de desarrollo:
   ```
   python manage.py runserver
   ```

Visite `http://localhost:8000` en su navegador para ver el proyecto en acción.
