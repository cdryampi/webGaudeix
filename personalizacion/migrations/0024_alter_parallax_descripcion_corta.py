# Generated by Django 4.2.2 on 2023-08-07 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalizacion', '0023_delete_carruselsubblog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parallax',
            name='descripcion_corta',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
