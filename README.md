# Gaudeix

Gaudeix es un proyecto web desarrollado con Django que tiene como objetivo migrar y mejorar una web existente actualmente en un CMS privado. La motivación detrás de este proyecto es reemplazar el CMS actual, que no recibe mantenimiento, presenta un backoffice poco intuitivo y carece de medidas de seguridad adecuadas.

## Características principales

- Registro y control de usuarios.
- Gestión de suscriptores: los usuarios pueden agregar, editar y eliminar suscriptores de su lista de correo.
- Envío de correos electrónicos: integraremos Teenvio.
- Personalización del sitio web: los usuarios pueden personalizar la apariencia del sitio web, incluido el logotipo, el favicon y otros componentes estáticos.
- Blog: los usuarios pueden crear, editar y publicar contenido en forma de entradas de blog, categorías y subblogs.

## Estructura del proyecto

El proyecto está organizado en diferentes aplicaciones que sirven propósitos específicos:

- **Users**: maneja el control y el registro de usuarios internos.
- **API**: proporciona una API externa para el envío de correos electrónicos utilizando la plataforma Teenvio.
- **Email**: contiene el modelo y la lógica relacionada con el envío de correos electrónicos.
- **Subscriber**: se encarga de la gestión de suscriptores y la suscripción a la newsletter.
- **Footer**: gestiona los componentes visuales del pie de página del sitio web.
- **Configuracion**: se encarga de la personalización del sitio web, como el logotipo y el favicon.
- **Blog**: maneja el contenido del blog, incluyendo las entradas, las categorías y los subblogs.

## Configuración del entorno de desarrollo

Para configurar el entorno de desarrollo de Gaudeix, sigue los siguientes pasos:

1. Clona el repositorio de Gaudeix en tu máquina local.
2. Crea un entorno virtual y activa el entorno virtual.
3. Instala las dependencias del proyecto utilizando el archivo `requirements.txt`.
4. Realiza las migraciones de la base de datos.
5. Inicia el servidor de desarrollo de Django.

## Contribución

Si deseas contribuir a Gaudeix, por favor sigue los siguientes pasos:

1. Haz un fork del repositorio de Gaudeix.
2. Crea una rama para tu nueva función o mejora.
3. Realiza los cambios necesarios y realiza los commits.
4. Envía una solicitud de pull con tus cambios.

¡Esperamos que disfrutes utilizando Gaudeix y que esta migración a Django mejore significativamente la funcionalidad, el diseño y la seguridad de tu web existente!

