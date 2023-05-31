# Generated by Django 3.2.19 on 2023-05-31 07:33

import ckeditor.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multimedia_manager', '0005_fichero'),
        ('blog', '0045_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Data de creació')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, help_text='Data de modificació')),
                ('metatitulo', models.CharField(blank=True, help_text='Metatítol per a SEO', max_length=255, null=True)),
                ('metadescripcion', models.TextField(blank=True, help_text='Metadescripció per a SEO', null=True)),
                ('titulo', models.CharField(max_length=255)),
                ('imagen', models.ImageField(upload_to='eventos/')),
                ('fecha', models.DateField(default=datetime.datetime(2023, 5, 31, 7, 33, 26, 590916, tzinfo=utc))),
                ('hora_inicio', models.TimeField(default=datetime.datetime(2023, 5, 31, 0, 0, 26, 590916, tzinfo=utc))),
                ('hora_fin', models.TimeField(default=datetime.datetime(2023, 5, 31, 1, 0, 26, 590916, tzinfo=utc))),
                ('ubicacion', models.CharField(max_length=255)),
                ('descripcion_corta', models.CharField(max_length=255)),
                ('descripcion_larga', ckeditor.fields.RichTextField()),
                ('creado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agenda_creados', to=settings.AUTH_USER_MODEL)),
                ('modificado_por', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, to='blog.Tag')),
            ],
            options={
                'verbose_name': 'Agenda',
                'verbose_name_plural': 'Agendas',
            },
        ),
        migrations.CreateModel(
            name='GaleriaAgenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agenda', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='agenda.agenda')),
                ('imagen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='multimedia_manager.imagen')),
            ],
        ),
    ]
