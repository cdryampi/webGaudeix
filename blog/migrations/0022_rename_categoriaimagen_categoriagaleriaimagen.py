# Generated by Django 4.2.1 on 2023-05-18 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0002_alter_imagen_archivo'),
        ('blog', '0021_remove_categoria_imagenes_categoriaimagen_categoria'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CategoriaImagen',
            new_name='CategoriaGaleriaImagen',
        ),
    ]
