from django.shortcuts import render

# Create your views here.

def error_404(request, exception):
    return render(request, 'core/404/error.html', {'message': 'Página no encontrada'})