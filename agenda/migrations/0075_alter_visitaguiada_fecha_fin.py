# Generated by Django 4.2.2 on 2023-08-07 09:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0074_alter_visitaguiada_fecha_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2023, 8, 14, 9, 21, 56, 975131, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang'),
        ),
    ]
