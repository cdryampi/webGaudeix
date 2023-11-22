# Generated by Django 4.2.2 on 2023-11-13 12:07

from django.db import migrations, models
import django.db.models.deletion
import personalizacion.utils


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia_manager', '0014_alter_fichero_options_alter_imagen_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parallax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Títol')),
                ('descripcion_corta', models.CharField(blank=True, max_length=200, null=True, verbose_name='Descripció curta')),
                ('imagen', models.ImageField(upload_to=personalizacion.utils.get_parallax_image_path, verbose_name='Imatge')),
                ('publicado', models.BooleanField(default=False, verbose_name='Publicat')),
            ],
        ),
        migrations.CreateModel(
            name='VideosEmbed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(help_text='Títol del Vídeo.', max_length=100, verbose_name='Títol')),
                ('publicado', models.BooleanField(default=False, verbose_name='Publicat')),
                ('video', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='multimedia_manager.video')),
            ],
        ),
    ]