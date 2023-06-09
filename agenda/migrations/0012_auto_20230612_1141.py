# Generated by Django 3.2.19 on 2023-06-12 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_mappoint_publicado'),
        ('agenda', '0011_visitaguidada_visitaguidadagaleriaimagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitaguidada',
            name='agendas',
            field=models.ManyToManyField(blank=True, help_text='Agendes relacionades amb la visita', related_name='visitas_guiadas', to='agenda.Agenda'),
        ),
        migrations.AlterField(
            model_name='visitaguidada',
            name='duracion',
            field=models.DurationField(default='2 days', help_text='Duració de la visita (en format DD HH:MM:SS)'),
        ),
        migrations.AlterField(
            model_name='visitaguidada',
            name='mapa',
            field=models.ForeignKey(blank=True, help_text='Mapa relacionat amb la visita', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visitas_mapa', to='map.mappoint'),
        ),
        migrations.AlterField(
            model_name='visitaguidada',
            name='precio',
            field=models.DecimalField(decimal_places=2, help_text='Preu de la visita (en euros)', max_digits=8),
        ),
        migrations.AlterField(
            model_name='visitaguidada',
            name='publico_recomendado',
            field=models.CharField(choices=[('nens', 'Nens'), ('joves', 'Joves'), ('adults', 'Adults'), ('todos', 'Totes les edats')], default='todos', help_text='Públic recomanat per a la visita', max_length=20),
        ),
        migrations.AlterField(
            model_name='visitaguidada',
            name='punto_inicio',
            field=models.ForeignKey(blank=True, help_text='Mapa relacionat amb la visita', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visitas_punto_inicio', to='map.mappoint'),
        ),
    ]
