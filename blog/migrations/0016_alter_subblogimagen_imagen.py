# Generated by Django 4.2.1 on 2023-05-18 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0002_alter_imagen_archivo'),
        ('blog', '0015_remove_subblog_imagen_subblogimagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subblogimagen',
            name='imagen',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='multimedia_manager.imagen'),
        ),
    ]