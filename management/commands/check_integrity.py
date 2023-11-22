from django.core.management.base import BaseCommand
# Importa tu función de check_integrity aquí

class Command(BaseCommand):
    help = 'Comprueba la integridad de los datos del modelo'

    def handle(self, *args, **kwargs):
        errors = check_integrity_subblog()  # Suponiendo que esta es tu función de comprobación
        if errors:
            for error in errors:
                self.stdout.write(self.style.ERROR(error))
        else:
            self.stdout.write(self.style.SUCCESS('No se encontraron problemas de integridad.'))
