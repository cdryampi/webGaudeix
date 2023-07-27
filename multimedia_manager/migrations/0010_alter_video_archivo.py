# Generated by Django 4.2.2 on 2023-07-27 11:29

from django.db import migrations, models
import multimedia_manager.utils


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0009_alter_video_archivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='archivo',
            field=models.FileField(blank=True, default=None, help_text='Extensiones permitidas: .mp4, .avi, .mov, .mkv', null=True, upload_to=multimedia_manager.utils.upload_to_fichero),
        ),
    ]
