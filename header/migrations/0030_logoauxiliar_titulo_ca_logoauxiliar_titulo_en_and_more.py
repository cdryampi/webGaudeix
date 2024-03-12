# Generated by Django 4.2.2 on 2024-03-11 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0029_logoauxiliar'),
    ]

    operations = [
        migrations.AddField(
            model_name='logoauxiliar',
            name='titulo_ca',
            field=models.CharField(blank=True, help_text='Títol opcional per al logo.', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='logoauxiliar',
            name='titulo_en',
            field=models.CharField(blank=True, help_text='Títol opcional per al logo.', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='logoauxiliar',
            name='titulo_es',
            field=models.CharField(blank=True, help_text='Títol opcional per al logo.', max_length=100, null=True),
        ),
    ]