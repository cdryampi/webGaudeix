# Generated by Django 4.2 on 2023-05-19 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0027_alter_subblog_contenido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subblog',
            name='contenido',
            field=models.TextField(help_text='Contingut del subblog'),
        ),
    ]