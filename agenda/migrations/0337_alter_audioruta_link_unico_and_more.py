# Generated by Django 4.2.2 on 2024-02-26 10:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0336_alter_visitaguiada_fecha_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audioruta',
            name='link_unico',
            field=models.CharField(blank=True, help_text="Afegeix un enllaç 'https://gaudeixcabrera.cat/redirect/meu_fitxer.mp3'", null=True, unique=True, verbose_name='Afegeix un enllaç unic'),
        ),
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2024, 3, 4, 10, 36, 54, 235077, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang', verbose_name='Data de finalització'),
        ),
    ]
