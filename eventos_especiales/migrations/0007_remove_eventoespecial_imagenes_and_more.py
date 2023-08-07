# Generated by Django 4.2.2 on 2023-08-07 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0011_alter_video_archivo'),
        ('eventos_especiales', '0006_eventoespecial_fecha_fin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventoespecial',
            name='imagenes',
        ),
        migrations.AddField(
            model_name='eventoespecial',
            name='imagenes',
            field=models.ForeignKey(blank=True, help_text="Imatges de l'esdeveniment especial (mínim 4)", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eventos_especiales', to='multimedia_manager.imagen'),
        ),
    ]
