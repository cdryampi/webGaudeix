# Generated by Django 3.2.19 on 2023-05-31 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0005_auto_20230531_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agenda',
            name='descripcion_larga',
        ),
        migrations.RemoveField(
            model_name='agenda',
            name='fecha',
        ),
        migrations.RemoveField(
            model_name='agenda',
            name='hora_fin',
        ),
        migrations.RemoveField(
            model_name='agenda',
            name='hora_inicio',
        ),
        migrations.RemoveField(
            model_name='agenda',
            name='imagen',
        ),
        migrations.RemoveField(
            model_name='agenda',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='agenda',
            name='titulo',
        ),
        migrations.DeleteModel(
            name='GaleriaAgenda',
        ),
    ]
