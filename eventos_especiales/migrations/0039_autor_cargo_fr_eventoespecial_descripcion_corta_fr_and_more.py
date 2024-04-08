# Generated by Django 4.2.2 on 2024-04-06 20:40

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos_especiales', '0038_alter_eventoespecial_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='autor',
            name='cargo_fr',
            field=models.CharField(max_length=100, null=True, verbose_name='càrrec'),
        ),
        migrations.AddField(
            model_name='eventoespecial',
            name='descripcion_corta_fr',
            field=ckeditor.fields.RichTextField(blank=True, help_text="Descripció curta de l'esdeveniment especial", null=True, verbose_name='Descripció curta'),
        ),
        migrations.AddField(
            model_name='eventoespecial',
            name='descripcion_larga_fr',
            field=ckeditor.fields.RichTextField(blank=True, help_text="Descripció llarga de l'esdeveniment especial", null=True, verbose_name='Descripció llarga'),
        ),
        migrations.AddField(
            model_name='eventoespecial',
            name='titulo_fr',
            field=models.CharField(help_text="Títol de l'esdeveniment especial", max_length=255, null=True, verbose_name='Títol'),
        ),
        migrations.AddField(
            model_name='medidaeconomica',
            name='descripcion_fr',
            field=models.TextField(help_text='Afegeix la descripció de la mesura econòmica per la web(sortirà el popup).', null=True, verbose_name='Descripció'),
        ),
        migrations.AddField(
            model_name='medidaeconomica',
            name='titulo_html_fr',
            field=models.CharField(help_text='Afegeix el títol de la mesura per la web.', max_length=200, null=True, verbose_name='Títol de la mesura'),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='contenido_fr',
            field=ckeditor.fields.RichTextField(help_text="Afegeix un missatge per l'esdeveniment", null=True, verbose_name='comentari'),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='mensaje_despedida_fr',
            field=models.CharField(blank=True, help_text="Afegeix un missatge de comiat, per exemple: 'Bon Nadal' o 'Bon Nadal i feliç 2023!'", max_length=255, null=True, verbose_name='Missatge de comiat'),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='titulo_fr',
            field=models.CharField(help_text="Afegeix el títol del missatge, per exemple: 'Dies de família, dies de poble' o 'Les entitats, pilar fonamental de Nadal'", max_length=255, null=True, verbose_name='Títol'),
        ),
    ]
