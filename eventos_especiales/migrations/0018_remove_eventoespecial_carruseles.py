# Generated by Django 4.2.2 on 2023-11-13 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos_especiales', '0017_alter_eventoespecial_qr_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventoespecial',
            name='carruseles',
        ),
    ]