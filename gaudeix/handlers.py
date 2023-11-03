# tu_app_principal/handlers.py

import logging
from admin_utils.models import RegistroError

class BaseExceptionHandler(logging.Handler):
    def emit(self, record):
        mensaje = self.format(record)
        RegistroError.objects.create(mensaje=mensaje)

class Excepcion500Handler(BaseExceptionHandler):
    def emit(self, record):
        if record.exc_info:
            return super().emit(record)
