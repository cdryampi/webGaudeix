# Generated by Django 4.2.2 on 2023-08-14 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0012_alter_fichero_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichero',
            name='titulo',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]