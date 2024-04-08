# Generated by Django 4.2.2 on 2024-04-06 20:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topbar', '0014_alter_topbar_descripcion_corta_movil_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='topbar',
            name='descripcion_corta_movil_fr',
            field=models.CharField(blank=True, help_text='Descripció curta per a mòbils (màxim 50 paraules)', max_length=50, null=True, verbose_name='Descripció curta per a mòbils'),
        ),
        migrations.AddField(
            model_name='topbar',
            name='descripcion_fr',
            field=models.TextField(help_text='Descripció del TopBar', null=True, validators=[django.core.validators.MaxLengthValidator(200)], verbose_name='Descripció del TopBar'),
        ),
        migrations.AddField(
            model_name='topbar',
            name='titulo_externo_fr',
            field=models.CharField(blank=True, help_text='nom enllaç màxim 20 paraules', max_length=25, null=True, verbose_name='Nom enllaç'),
        ),
        migrations.AddField(
            model_name='topbar',
            name='titulo_fr',
            field=models.CharField(help_text='Títol del TopBar', max_length=100, null=True, verbose_name='Títol del TopBar'),
        ),
    ]
