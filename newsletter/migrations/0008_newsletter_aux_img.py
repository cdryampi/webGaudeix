# Generated by Django 4.2.2 on 2024-04-06 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0007_newsletter_html_file_fr_newsletter_subtitulo_fr'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='aux_img',
            field=models.ImageField(help_text="Fes servir aquest model d'imatge per afegir un banner al mig de la newsteller.", null=True, upload_to='aux_img_newsletter', verbose_name='Imatge auxiliar'),
        ),
    ]
