# Generated by Django 4.2 on 2023-05-22 13:30

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0041_remove_post_meta_descripcion_remove_post_meta_titulo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subblog',
            name='contenido',
            field=ckeditor.fields.RichTextField(help_text='Contingut del subblog'),
        ),
    ]
