# Generated by Django 4.2.2 on 2024-03-11 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0031_remove_header_logo_auxiliar_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logoauxiliar',
            options={'ordering': ['orden']},
        ),
        migrations.AddField(
            model_name='logoauxiliar',
            name='orden',
            field=models.PositiveIntegerField(default=0, verbose_name='Ordre'),
        ),
    ]