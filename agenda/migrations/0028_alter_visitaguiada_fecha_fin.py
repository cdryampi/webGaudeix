# Generated by Django 4.2.2 on 2023-07-07 07:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0027_alter_visitaguiada_fecha_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2023, 7, 14, 7, 4, 29, 911398, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang'),
        ),
    ]
