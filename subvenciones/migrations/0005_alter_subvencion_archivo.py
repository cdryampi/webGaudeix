# Generated by Django 4.2.2 on 2023-08-11 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subvenciones', '0004_subvenciondescripcion_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subvencion',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='subvenciones/'),
        ),
    ]