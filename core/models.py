from django.db import models

class BaseModel(models.Model):
    # Agrega aquí los campos y atributos que desees para tu modelo base
    # por ejemplo, puedes agregar campos para recursos estáticos, plantillas, etc.

    class Meta:
        abstract = True
