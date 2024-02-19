# Generated by Django 4.2.2 on 2024-02-16 10:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerta', '0007_alerta_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='alerta',
            name='descripcion_ca',
            field=models.TextField(help_text="Escriu una descripció detallada de l'alerta", max_length=255, null=True, validators=[django.core.validators.MaxLengthValidator(255)], verbose_name='descripció'),
        ),
        migrations.AddField(
            model_name='alerta',
            name='descripcion_en',
            field=models.TextField(help_text="Escriu una descripció detallada de l'alerta", max_length=255, null=True, validators=[django.core.validators.MaxLengthValidator(255)], verbose_name='descripció'),
        ),
        migrations.AddField(
            model_name='alerta',
            name='descripcion_es',
            field=models.TextField(help_text="Escriu una descripció detallada de l'alerta", max_length=255, null=True, validators=[django.core.validators.MaxLengthValidator(255)], verbose_name='descripció'),
        ),
        migrations.AddField(
            model_name='alerta',
            name='titulo_ca',
            field=models.CharField(help_text="Introdueix el títol de l'alerta", max_length=200, null=True, verbose_name='títol'),
        ),
        migrations.AddField(
            model_name='alerta',
            name='titulo_en',
            field=models.CharField(help_text="Introdueix el títol de l'alerta", max_length=200, null=True, verbose_name='títol'),
        ),
        migrations.AddField(
            model_name='alerta',
            name='titulo_es',
            field=models.CharField(help_text="Introdueix el títol de l'alerta", max_length=200, null=True, verbose_name='títol'),
        ),
    ]
