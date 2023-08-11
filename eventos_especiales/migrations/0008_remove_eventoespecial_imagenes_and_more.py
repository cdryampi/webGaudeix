# Generated by Django 4.2.2 on 2023-08-07 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0011_alter_video_archivo'),
        ('eventos_especiales', '0007_remove_eventoespecial_imagenes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventoespecial',
            name='imagenes',
        ),
        migrations.CreateModel(
            name='EventoEspecialGaleriaImagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evento_especial', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='eventos_especiales.eventoespecial')),
                ('imagen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='multimedia_manager.imagen')),
            ],
        ),
    ]