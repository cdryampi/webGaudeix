Proyecto Gaudeix
Descripción
El proyecto Gaudeix es un blog de turismo y fiestas, desarrollado utilizando el framework Django. La web está orientada a promover destinos turísticos y eventos festivos, centrándose principalmente en la región de Cataluña. El sitio web está completamente en catalán y ofrece contenido relacionado con viajes, atracciones turísticas, festividades y recomendaciones para los visitantes.

Estructura del proyecto
csharp
Copy code
gaudeix/
├── gaudeix/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── blog/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   │   └── blog/
│   │       └── ...
│   └── ...
├── legal/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   │   └── legal/
│   │       └── ...
│   └── ...
├── base/
│   ├── templates/
│   │   └── base/
│   │       └── base.html
│   └── static/
