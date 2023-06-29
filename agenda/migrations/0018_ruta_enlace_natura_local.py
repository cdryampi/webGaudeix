# Generated by Django 4.2.2 on 2023-06-29 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0017_ruta'),
    ]

    operations = [
        migrations.AddField(
            model_name='ruta',
            name='enlace_natura_local',
            field=models.URLField(default='https://naturalocal.net/ca/destins/barcelona/cabrera-de-mar#rutes', help_text="Afegeix l'enllaç exacte cap a Natura Local."),
        ),
    ]
