# Generated by Django 4.2.2 on 2023-07-04 09:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0023_alter_visitaguiada_fecha_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2023, 7, 11, 9, 27, 5, 882293, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang'),
        ),
    ]
