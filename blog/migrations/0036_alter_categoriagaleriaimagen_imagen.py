# Generated by Django 4.2 on 2023-05-22 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0005_fichero'),
        ('blog', '0035_alter_postgaleriaimagen_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriagaleriaimagen',
            name='imagen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='multimedia_manager.imagen'),
        ),
    ]