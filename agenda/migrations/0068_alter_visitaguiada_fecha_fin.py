# Generated by Django 4.2.2 on 2023-08-03 17:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0067_alter_visitaguiada_fecha_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2023, 8, 10, 17, 36, 33, 228875, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang'),
        ),
    ]
