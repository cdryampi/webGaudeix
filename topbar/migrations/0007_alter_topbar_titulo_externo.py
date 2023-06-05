# Generated by Django 4.2 on 2023-05-25 10:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topbar', '0006_remove_topbar_titulo_extermo_topbar_titulo_externo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topbar',
            name='titulo_externo',
            field=models.CharField(blank=True, help_text='nom enllaç màxim 10 paraules', null=True, validators=[django.core.validators.MaxLengthValidator(10)]),
        ),
    ]