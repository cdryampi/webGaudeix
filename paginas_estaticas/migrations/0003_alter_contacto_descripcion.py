# Generated by Django 4.2.2 on 2023-06-16 07:01

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paginas_estaticas', '0002_delete_agenda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='descripcion',
            field=ckeditor.fields.RichTextField(help_text='Descripción del contacto'),
        ),
    ]
