# Generated by Django 4.2.1 on 2023-05-17 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_subblog_imagen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subblog',
            name='imagen',
        ),
    ]
