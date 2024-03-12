# Generated by Django 4.2.2 on 2024-02-28 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0024_imagencarrusel_descripcion_ca_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrusel',
            name='tipo',
            field=models.CharField(choices=[('carrusel', 'Carrusel'), ('collage', 'Collage')], default='carrusel', max_length=8, verbose_name='Tipus de visualització'),
        ),
    ]