# Generated by Django 4.2.2 on 2023-08-18 07:37

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0014_mappoint_calle_mappoint_codigo_postal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mappoint',
            name='enlace_google_maps',
            field=models.URLField(blank=True, help_text='Enllaç a Google Maps', null=True, verbose_name='Enllaç a Google Maps'),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='calle',
            field=models.CharField(blank=True, help_text='Carrer', max_length=255, null=True, verbose_name='Carrer'),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='codigo_postal',
            field=models.CharField(default='08349', editable=False, help_text='Codi postal', max_length=10, verbose_name='Codi postal'),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='comarca',
            field=models.CharField(default='Maresme', editable=False, help_text='Comarca', max_length=100, verbose_name='Comarca'),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='comunidad_autonoma',
            field=models.CharField(default='Catalunya', editable=False, help_text='Comunitat Autònoma', max_length=100, verbose_name='Comunitat Autònoma'),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='contenido_adicional',
            field=ckeditor.fields.RichTextField(blank=True, help_text='Texto adicional', null=True, verbose_name='Contingut addicional'),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='latitud',
            field=models.FloatField(help_text='Introduïu la latitud (copiada de Google Maps)', verbose_name='Latitud'),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='longitud',
            field=models.FloatField(help_text='Introduïu la longitud (copiada de Google Maps)', verbose_name='Longitud'),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='municipio',
            field=models.CharField(default='Cabrera de Mar', editable=False, help_text='Municipi', max_length=100, verbose_name='Municipi'),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='pais',
            field=models.CharField(default='Espanya', editable=False, help_text='País', max_length=100, verbose_name='País'),
        ),
    ]
