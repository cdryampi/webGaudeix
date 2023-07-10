# Generated by Django 4.2.2 on 2023-07-10 10:34

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0005_alter_referencia_options_referencia_orden'),
    ]

    operations = [
        migrations.AddField(
            model_name='referencia',
            name='color_fondo_header',
            field=colorfield.fields.ColorField(default='#0000', image_field=None, max_length=18, samples=None),
        ),
        migrations.AddField(
            model_name='referencia',
            name='color_letra',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None),
        ),
    ]