# Generated by Django 4.2.2 on 2023-07-10 10:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0037_alter_visitaguiada_fecha_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2023, 7, 17, 10, 36, 42, 806436, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang'),
        ),
    ]