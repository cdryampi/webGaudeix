# Generated by Django 4.2.2 on 2024-02-26 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0021_carrusel_imagencarrusel'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagencarrusel',
            name='descripcion',
            field=models.TextField(blank=True, help_text="Descripció per l'imatge que sortirà a la web.", null=True, verbose_name='Caption'),
        ),
        migrations.AlterField(
            model_name='carrusel',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripció intern'),
        ),
        migrations.AlterField(
            model_name='carrusel',
            name='titulo',
            field=models.CharField(max_length=100, verbose_name='Títol del Carrusel intern'),
        ),
    ]