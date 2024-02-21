# Generated by Django 4.2.2 on 2024-01-19 07:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0276_remove_ruta_playlist_alter_visitaguiada_fecha_fin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ruta',
            name='playlist',
            field=models.ManyToManyField(blank=True, to='agenda.playlistruta', verbose_name='Playlist'),
        ),
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2024, 1, 26, 7, 26, 24, 601334, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang', verbose_name='Data de finalització'),
        ),
    ]