from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import PaginaLegal


def privacitat(request):
    pagina = PaginaLegal.objects.get(tipo='privacitat')
    print(pagina.imagen)  # Imprimir el objeto pagina en la consola
    return render(request, 'legal/privacitat.html', {'legal': pagina})

def avis_legal(request):
    pagina = PaginaLegal.objects.get(tipo='avis_legal')
    print(pagina)  # Imprimir el objeto pagina en la consola
    return render(request, 'legal/avis_legal.html', {'legal': pagina})

def politica_cookies(request):
    pagina = PaginaLegal.objects.get(tipo='cookies')
    print(pagina)  # Imprimir el objeto pagina en la consola
    return render(request, 'legal/politica_cookies.html', {'legal': pagina})
