# Generated by Django 4.2.2 on 2024-02-23 12:59

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0023_enlaceexterno_titulo_ca_enlaceexterno_titulo_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='header',
            name='color_entrada',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None),
        ),
    ]