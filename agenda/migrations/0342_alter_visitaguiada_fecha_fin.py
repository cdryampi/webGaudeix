# Generated by Django 4.2.2 on 2024-02-26 14:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0341_alter_visitaguiada_fecha_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2024, 3, 4, 14, 52, 40, 87742, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang', verbose_name='Data de finalització'),
        ),
    ]
