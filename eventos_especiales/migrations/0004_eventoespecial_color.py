# Generated by Django 4.2.2 on 2023-07-07 10:02

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos_especiales', '0003_alter_eventoespecial_descripcion_corta'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventoespecial',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None),
        ),
    ]