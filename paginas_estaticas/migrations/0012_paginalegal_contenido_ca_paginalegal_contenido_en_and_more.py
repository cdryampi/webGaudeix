# Generated by Django 4.2.2 on 2024-02-13 12:47

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paginas_estaticas', '0011_paginalegal_encabezado_ca_paginalegal_encabezado_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paginalegal',
            name='contenido_ca',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='paginalegal',
            name='contenido_en',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='paginalegal',
            name='contenido_es',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
