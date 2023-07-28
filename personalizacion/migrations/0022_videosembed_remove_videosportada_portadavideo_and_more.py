# Generated by Django 4.2.2 on 2023-07-26 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0009_alter_video_archivo'),
        ('personalizacion', '0021_remove_videosportada_orden_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideosEmbed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('publicado', models.BooleanField(default=False)),
                ('videos', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='multimedia_manager.video')),
            ],
        ),
        migrations.RemoveField(
            model_name='videosportada',
            name='portadavideo',
        ),
        migrations.RemoveField(
            model_name='videosportada',
            name='videos',
        ),
        migrations.DeleteModel(
            name='PortadaVideo',
        ),
        migrations.DeleteModel(
            name='VideosPortada',
        ),
    ]