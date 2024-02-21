# Generated by Django 4.2.2 on 2024-02-06 10:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0298_alter_visitaguiada_fecha_fin'),
    ]

    operations = [
        migrations.AddField(
            model_name='alojamiento',
            name='adaptado_movilidad_reducida',
            field=models.BooleanField(default=False, help_text="Indica si l'allotjament està adaptat per a persones amb mobilitat reduïda.", verbose_name='Adaptat per a persones amb mobilitat reduïda'),
        ),
        migrations.AddField(
            model_name='alojamiento',
            name='habitaciones_sin_humo',
            field=models.BooleanField(default=False, help_text="Indica si l'allotjament disposa d'habitacions lliures de fum.", verbose_name='Habitacions sense fum'),
        ),
        migrations.AddField(
            model_name='alojamiento',
            name='parking_gratis',
            field=models.BooleanField(default=False, help_text="Indica si l'allotjament ofereix pàrquing gratuït.", verbose_name='Pàrquing gratuït'),
        ),
        migrations.AddField(
            model_name='alojamiento',
            name='servicio_habitaciones',
            field=models.BooleanField(default=False, help_text="Indica si l'allotjament ofereix servei d'habitacions.", verbose_name="Servei d'habitacions"),
        ),
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2024, 2, 13, 10, 12, 2, 270330, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang', verbose_name='Data de finalització'),
        ),
    ]