# Generated by Django 4.2.2 on 2023-07-27 07:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0056_alter_visitaguiada_fecha_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2023, 8, 3, 7, 42, 56, 243788, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang'),
        ),
    ]
