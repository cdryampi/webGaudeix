# Generated by Django 4.2.2 on 2024-04-23 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0034_enlaceexterno_titulo_fr_logoauxiliar_titulo_fr'),
    ]

    operations = [
        migrations.AddField(
            model_name='logoauxiliar',
            name='mostrar_portada',
            field=models.BooleanField(default=False, help_text='Indica si vols que la imatge surti a la portada.', verbose_name='mostrar portada'),
        ),
    ]