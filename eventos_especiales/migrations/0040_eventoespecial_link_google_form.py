# Generated by Django 4.2.2 on 2024-04-15 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos_especiales', '0039_autor_cargo_fr_eventoespecial_descripcion_corta_fr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventoespecial',
            name='link_google_form',
            field=models.URLField(blank=True, help_text='Enllaç opcional pel formulari.', null=True),
        ),
    ]