# Generated by Django 4.2.2 on 2023-09-28 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compra_y_descubre', '0003_remove_compradescubre_agendas_compradescubre_negocis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compradescubre',
            name='parallax',
        ),
    ]
