from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import PaginaLegal

def privacitat(request):
    pagina = PaginaLegal.objects.get(tipo='privacitat')
    return render(request, 'legal/privacitat.html', {'pagina': pagina})

def avis_legal(request):
    pagina = PaginaLegal.objects.get(tipo='avis_legal')
    return render(request, 'legal/avis_legal.html', {'pagina': pagina})

def politica_cookies(request):
    pagina = PaginaLegal.objects.get(tipo='cookies')
    return render(request, 'legal/politica_cookies.html', {'pagina': pagina})
