# Generated by Django 4.2.2 on 2023-08-16 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos_especiales', '0009_eventoespecial_imagen_especial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventoespecial',
            name='metadescripcion',
            field=models.TextField(blank=True, help_text='Metadescripció per a SEO', null=True, verbose_name='Metadescripció'),
        ),
        migrations.AlterField(
            model_name='eventoespecial',
            name='metatitulo',
            field=models.CharField(blank=True, help_text='Metatítol per a SEO', max_length=255, null=True, verbose_name='Metatítol'),
        ),
    ]
