# Generated by Django 3.2.19 on 2023-05-31 08:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0002_auto_20230531_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2023, 5, 31, 8, 22, 39, 417531, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='hora_fin',
            field=models.TimeField(default=datetime.datetime(2023, 5, 31, 1, 0, 39, 417531, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='hora_inicio',
            field=models.TimeField(default=datetime.datetime(2023, 5, 31, 0, 0, 39, 417531, tzinfo=utc)),
        ),
    ]
