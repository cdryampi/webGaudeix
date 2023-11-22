from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings
from django.urls import reverse

class GaudeixQrFile(models.Model):
    file = models.FileField(upload_to='uploaded_files/')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if not self.qr_code:
            # Genera el código QR basándose en la URL absoluta del archivo
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.get_absolute_url())
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            qr_image.save(buffer, format="PNG")
            buffer.seek(0)

            # Asigna el código QR al campo 'qr_code'
            file_name = f'qr_{self.file.name}.png'
            self.qr_code.save(file_name, File(buffer), save=False)
            buffer.close()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Aquí deberías construir la URL absoluta del archivo
        return f"{settings.MEDIA_URL}{self.file.name}"

    def __str__(self):
        return f"Archivo: {self.file.name}"
