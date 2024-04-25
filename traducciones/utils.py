import re
import subprocess
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.contrib import messages

from .models import Translation
from .forms import POEditForm
from gaudeix.settings import SCRIPT_PATH

@staff_member_required
def edit_view(request, object_id):
    translation = get_object_or_404(Translation, pk=object_id)
    if request.method == 'POST':
        form = POEditForm(request.POST)
        if form.is_valid():
            # Eliminar tres o más saltos de línea consecutivos y reemplazarlos con dos saltos de línea
            content = re.sub(r'(\n\s*){3,}', '\n\n', form.cleaned_data['content'])
            # Normalizar los finales de línea a Unix
            content = content.replace('\r\n', '\n')
            translation.save_po_file_content(content)

            # Determinar el comando basado en el sistema operativo
            script_file = os.path.join(SCRIPT_PATH, 'compile_message.sh')
            compile_command = script_file
            if os.name == 'nt':  # Para Windows
                compile_command = ['python', '-m', 'django', 'compilemessages']

            try:
                subprocess.run(compile_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                messages.success(request, "Mensajes compilados exitosamente.")
            except subprocess.CalledProcessError as e:
                error_message = e.stderr.decode('utf-8') if e.stderr else 'Error desconocido al compilar mensajes.'
                messages.error(request, f"Hubo un error al compilar los mensajes: {error_message}")
            
            return redirect(reverse('admin:traducciones_translation_change', args=[translation.pk]))
    else:
        content = translation.get_po_file_content()
        form = POEditForm(initial={'content': content})

    context = {
        'form': form,
        'opts': Translation._meta,
        'original': translation,
    }
    return render(request, "admin/translation_edit.html", context)
