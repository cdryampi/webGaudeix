# Generated by Django 4.2.2 on 2023-08-11 09:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0110_alter_visitaguiada_fecha_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2023, 8, 18, 9, 46, 2, 344784, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang'),
        ),
    ]