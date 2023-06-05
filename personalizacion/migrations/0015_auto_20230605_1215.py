# Generated by Django 3.2.19 on 2023-06-05 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0007_video'),
        ('personalizacion', '0014_portadavideo_videosportada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videosportada',
            name='video',
        ),
        migrations.AddField(
            model_name='videosportada',
            name='videos',
            field=models.ManyToManyField(to='multimedia_manager.Video'),
        ),
    ]