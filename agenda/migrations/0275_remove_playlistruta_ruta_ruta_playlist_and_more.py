# Generated by Django 4.2.2 on 2024-01-19 07:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0274_alter_audioruta_options_remove_audioruta_idioma_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlistruta',
            name='ruta',
        ),
        migrations.AddField(
            model_name='ruta',
            name='playlist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='agenda.playlistruta', verbose_name='Playlist'),
        ),
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2024, 1, 26, 7, 23, 13, 456396, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang', verbose_name='Data de finalització'),
        ),
    ]
