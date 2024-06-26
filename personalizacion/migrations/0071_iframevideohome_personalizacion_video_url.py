# Generated by Django 4.2.2 on 2024-04-16 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personalizacion', '0070_delete_iframevideohome'),
    ]

    operations = [
        migrations.CreateModel(
            name='IframeVideoHome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_name', models.CharField(help_text='Nom intern per identificar el vídeo dins del sistema.', max_length=255, verbose_name='Nom intern')),
                ('title', models.CharField(help_text='Títol del vídeo que es mostrarà públicament.', max_length=255, verbose_name='Títol')),
                ('description', models.TextField(help_text='Descripció detallada del contingut del vídeo.', verbose_name='Descripció')),
                ('video_url', models.URLField(help_text="URL de l'iframe del vídeo. Utilitza URLs que respectin la privacitat com 'youtube-nocookie' per a YouTube.", verbose_name='URL del vídeo')),
            ],
        ),
        migrations.AddField(
            model_name='personalizacion',
            name='video_url',
            field=models.OneToOneField(blank=True, help_text="Selecciona el vídeo auxiliar per a la portada (si n'hi ha un).", null=True, on_delete=django.db.models.deletion.SET_NULL, to='personalizacion.iframevideohome', verbose_name='Vídeo auxiliar per la portada'),
        ),
    ]
