# Generated by Django 4.2 on 2023-05-25 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personalizacion', '0002_alter_internallink_slide'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slide',
            name='carrusel',
        ),
    ]
