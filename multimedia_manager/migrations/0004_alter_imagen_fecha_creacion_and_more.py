# Generated by Django 4.2 on 2023-05-19 08:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0003_imagen_creado_por_imagen_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Data de creació'),
        ),
        migrations.AlterField(
            model_name='imagen',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True, help_text='Data de modificació'),
        ),
    ]
