# Generated by Django 4.2.2 on 2023-11-13 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos_especiales', '0018_remove_eventoespecial_carruseles'),
        ('personalizacion', '0037_personalizacion_parallax_agenda'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internallink',
            name='slide',
        ),
        migrations.DeleteModel(
            name='Carrusel',
        ),
        migrations.DeleteModel(
            name='Slide',
        ),
    ]