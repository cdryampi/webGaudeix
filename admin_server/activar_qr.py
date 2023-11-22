from eventos_especiales.models import EventoEspecial
from compra_y_descubre.models import CompraDescubre

eventos = EventoEspecial.objects.all()
compra_y_descubre = CompraDescubre.objects.all()

for evento in eventos:
    evento.save()

for c in compra_y_descubre:
    c.save()

