# Generated by Django 4.2.2 on 2023-12-04 12:21

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos_especiales', '0028_alter_autor_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='contenido',
            field=ckeditor.fields.RichTextField(help_text="Afegeix un missatge per l'esdeveniment", verbose_name='comentari'),
        ),
    ]
