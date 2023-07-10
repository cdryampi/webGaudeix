# Generated by Django 4.2.2 on 2023-07-04 09:05

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0021_alter_agenda_fecha_alter_agenda_hora'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitaguiada',
            name='punto_inicio',
        ),
        migrations.AddField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2023, 7, 11, 9, 5, 58, 7315, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang'),
        ),
        migrations.AddField(
            model_name='visitaguiada',
            name='fecha_inicio',
            field=models.DateField(default=django.utils.timezone.now, help_text="Data d'inici del rang"),
        ),
        migrations.AddField(
            model_name='visitaguiada',
            name='mostrar_calendario',
            field=models.CharField(choices=[('si', 'Sí'), ('no', 'No')], default='no', help_text='Indica si es mostrarà el calendari en la plantilla', max_length=2),
        ),
    ]