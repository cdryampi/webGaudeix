#!/bin/bash

# Ruta al archivo de activación del entorno virtual
VENV_ACTIVATE="/home/gaudeix/gaudeix_env/bin/activate"

# Verificar si el archivo de activación del entorno virtual existe
if [ -f "$VENV_ACTIVATE" ]; then
    # Activar el entorno virtual
    source "$VENV_ACTIVATE"

    # Ejecutar el comando django-admin compilemessages
    cd /home/gaudeix/webGaudeix
    # Ejecutar el comando django-admin compilemessages
    python manage.py compilemessages
    # Recargar Apache sin sudo
    echo "$password" | sudo -S systemctl reload apache2
else
    echo "El archivo de activación del entorno virtual no existe: $VENV_ACTIVATE"
fi