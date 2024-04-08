# Generated by Django 4.2.2 on 2024-04-06 20:40

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra_y_descubre', '0018_alter_compradescubre_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='compradescubre',
            name='descripcion_corta_fr',
            field=ckeditor.fields.RichTextField(blank=True, help_text="Descripció curta de l'esdeveniment Compra i descobreix", null=True, verbose_name='Descripció curta'),
        ),
        migrations.AddField(
            model_name='compradescubre',
            name='descripcion_larga_fr',
            field=ckeditor.fields.RichTextField(blank=True, help_text="Descripció llarga de l'esdeveniment Compra i descobreix", null=True, verbose_name='Descripció llarga'),
        ),
        migrations.AddField(
            model_name='compradescubre',
            name='titulo_fr',
            field=models.CharField(help_text='Títol pel compra i descobreix. PE: Compra i descobreix 2023', max_length=255, null=True, verbose_name='Títol'),
        ),
        migrations.AddField(
            model_name='compradescubrepasosimagen',
            name='descripcion_fr',
            field=ckeditor.fields.RichTextField(blank=True, help_text="Descripció del pas l'esdeveniment Compra i descobreix", null=True, verbose_name='Descripció curta'),
        ),
        migrations.AddField(
            model_name='compradescubrepasosimagen',
            name='titulo_fr',
            field=models.CharField(help_text='Títol pel compra i descobreix. PE: Pas 2A. Format paper', max_length=255, null=True, verbose_name='Títol'),
        ),
    ]