# Generated by Django 4.2.2 on 2023-09-14 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0017_alter_referencia_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referencia',
            name='tipo',
            field=models.CharField(choices=[('post', 'Post'), ('categoria', 'Categoría'), ('subblog', 'SubBlog'), ('externo', 'Enlace Externo'), ('contacto', 'Contacto'), ('evento_especial', 'evento_especial'), ('subvencion', 'Subvencion'), ('punt_informacio', 'punt_informació')], max_length=30),
        ),
    ]