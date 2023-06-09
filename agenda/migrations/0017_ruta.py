# Generated by Django 4.2.2 on 2023-06-27 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0007_alter_mappoint_icono'),
        ('blog', '0062_alter_post_titulo'),
        ('agenda', '0016_rename_visitaguidada_visitaguiada'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.post')),
                ('duracion', models.DurationField(blank=True, help_text='Durada de la ruta', null=True)),
                ('pendiente', models.FloatField(blank=True, help_text='Pendent de la ruta (en metres)', null=True)),
                ('distancia', models.FloatField(blank=True, help_text='Distància de la ruta (en quilòmetres)', null=True)),
                ('tema', models.CharField(blank=True, help_text='Tema de la ruta', max_length=255, null=True)),
                ('actividad', models.CharField(blank=True, help_text='Activitat de la ruta', max_length=255, null=True)),
                ('valoracion', models.FloatField(blank=True, help_text='Valoració de la ruta', null=True)),
                ('tipologia', models.CharField(choices=[('circular', 'Circular'), ('antihorario', 'Antihorari')], default='circular', help_text='Tipologia de la ruta', max_length=20, verbose_name='Tipologia')),
                ('dificultad', models.CharField(choices=[('facil', 'Fàcil'), ('media', 'Mitjana'), ('dificil', 'Difícil')], default='facil', help_text='Dificultat de la ruta', max_length=20, verbose_name='Dificultat')),
                ('mapas_itinerario', models.ManyToManyField(blank=True, help_text="Mapes que formen part de l'itinerari", related_name='rutas_itinerario', to='map.mappoint')),
                ('punto_inicio', models.ForeignKey(blank=True, help_text="Punt d'inici de la ruta", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rutas_punto_inicio', to='map.mappoint', verbose_name="Punt d'inici")),
            ],
            options={
                'abstract': False,
            },
            bases=('blog.post',),
        ),
    ]
