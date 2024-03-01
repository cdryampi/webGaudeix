# Generated by Django 4.2.2 on 2024-02-26 14:52

from django.db import migrations, models
import multimedia_manager.utils
import personalizacion.utils


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0022_imagencarrusel_descripcion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagencarrusel',
            name='imagen',
            field=models.ImageField(upload_to=personalizacion.utils.get_carrousel_image_path, validators=[multimedia_manager.utils.validar_tamanio_archivo], verbose_name='Imatge'),
        ),
    ]
