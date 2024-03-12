# Generated by Django 4.2.2 on 2024-03-11 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0027_header_logo_auxiliar'),
    ]

    operations = [
        migrations.AddField(
            model_name='header',
            name='logo_auxiliar_2',
            field=models.ImageField(blank=True, help_text='Logo auxiliar per afegir un logo del turisme sostenible.', null=True, upload_to='logo_auxiliar/'),
        ),
        migrations.AddField(
            model_name='header',
            name='logo_auxiliar_3',
            field=models.ImageField(blank=True, help_text='Logo auxiliar per afegir un logo del turisme sostenible.', null=True, upload_to='logo_auxiliar/'),
        ),
        migrations.AlterField(
            model_name='header',
            name='logo_auxiliar',
            field=models.ImageField(blank=True, help_text='Logo auxiliar per afegir un logo del turisme sostenible.', null=True, upload_to='logo_auxiliar/'),
        ),
    ]
