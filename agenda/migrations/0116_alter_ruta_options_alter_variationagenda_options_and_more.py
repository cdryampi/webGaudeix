# Generated by Django 4.2.2 on 2023-08-16 09:17

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0014_mappoint_calle_mappoint_codigo_postal_and_more'),
        ('agenda', '0115_alter_visitaguiada_fecha_fin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ruta',
            options={'verbose_name': 'Model de metadades', 'verbose_name_plural': 'Models de metadades'},
        ),
        migrations.AlterModelOptions(
            name='variationagenda',
            options={'verbose_name': "Variació d'agenda", 'verbose_name_plural': 'Variacions'},
        ),
        migrations.AlterField(
            model_name='agenda',
            name='descripcion_corta',
            field=models.CharField(max_length=255, verbose_name='Descripció curta'),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='entradas',
            field=models.BooleanField(default=False, help_text='Hi ha entrades?', verbose_name='Entrades'),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='tipo_evento',
            field=models.CharField(choices=[('musica', 'Música'), ('teatre', 'Teatre'), ('exposicio', 'Exposició'), ('festes', 'festes'), ('cinema', 'Cinema'), ('dansa', 'Dansa'), ('visites_guiades', 'Visites guiades'), ('activitats_turistiques', 'Activitats turístiques'), ('xerrades', 'xerrades'), ('joves', 'joves'), ('altres', 'Altres (Otros)')], default='altres', help_text="Selecciona el tipus d'esdeveniment", max_length=30, verbose_name="Tipus d'esdeveniment"),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='actividad',
            field=models.CharField(blank=True, help_text='Activitat de la ruta', max_length=255, null=True, verbose_name='Activitat'),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='distancia',
            field=models.FloatField(blank=True, help_text='Distància de la ruta (en quilòmetres)', null=True, verbose_name='Distància'),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='duracion',
            field=models.DurationField(blank=True, help_text='Durada de la ruta', null=True, verbose_name='Durada'),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='enlace_natura_local',
            field=models.URLField(default='https://naturalocal.net/ca/destins/barcelona/cabrera-de-mar#rutes', help_text="Afegeix l'enllaç exacte cap a Natura Local.", verbose_name='Enllaç a Natura Local'),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='mapas_itinerario',
            field=models.ManyToManyField(blank=True, help_text="Mapes que formen part de l'itinerari", related_name='rutas_itinerario', to='map.mappoint', verbose_name="Mapes d'itinerari"),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='pendiente',
            field=models.FloatField(blank=True, help_text='Pendent de la ruta (en metres)', null=True, verbose_name='Pendent'),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='tema',
            field=models.CharField(blank=True, help_text='Tema de la ruta', max_length=255, null=True, verbose_name='Tema'),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='valoracion',
            field=models.FloatField(blank=True, help_text='Valoració de la ruta', null=True, verbose_name='Valoració'),
        ),
        migrations.AlterField(
            model_name='variationagenda',
            name='agenda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.agenda', verbose_name='Agenda'),
        ),
        migrations.AlterField(
            model_name='variationagenda',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='variationagenda',
            name='hora',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Hora'),
        ),
        migrations.AlterField(
            model_name='visitaguiada',
            name='agendas',
            field=models.ManyToManyField(blank=True, help_text='Agendes relacionades amb la visita', related_name='visitas_guiadas', to='agenda.agenda', verbose_name='Agendes'),
        ),
        migrations.AlterField(
            model_name='visitaguiada',
            name='duracion',
            field=models.DurationField(default=datetime.timedelta(days=2), help_text='Duració de la visita (en format DD HH:MM:SS)', verbose_name='Duració'),
        ),
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2023, 8, 23, 9, 17, 34, 143092, tzinfo=datetime.timezone.utc), help_text='Data de finalització del rang', verbose_name='Data de finalització'),
        ),
        migrations.AlterField(
            model_name='visitaguiada',
            name='fecha_inicio',
            field=models.DateField(default=django.utils.timezone.now, help_text="Data d'inici del rang", verbose_name="Data d'inici"),
        ),
        migrations.AlterField(
            model_name='visitaguiada',
            name='mapa',
            field=models.ForeignKey(blank=True, help_text='Mapa relacionat amb la visita', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visitas_mapa', to='map.mappoint', verbose_name='Mapa'),
        ),
        migrations.AlterField(
            model_name='visitaguiada',
            name='mostrar_calendario',
            field=models.CharField(choices=[('si', 'Sí'), ('no', 'No')], default='no', help_text='Indica si es mostrarà el calendari en la plantilla', max_length=2, verbose_name='Mostrar calendari'),
        ),
        migrations.AlterField(
            model_name='visitaguiada',
            name='precio',
            field=models.DecimalField(decimal_places=2, help_text='Preu de la visita (en euros)', max_digits=8, verbose_name='Preu'),
        ),
        migrations.AlterField(
            model_name='visitaguiada',
            name='publico_recomendado',
            field=models.CharField(choices=[('nens', 'Nens'), ('joves', 'Joves'), ('adults', 'Adults'), ('todos', 'Totes les edats')], default='todos', help_text='Públic recomanat per a la visita', max_length=20, verbose_name='Públic recomanat'),
        ),
    ]
