# Generated by Django 4.2.2 on 2023-07-07 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos_especiales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventoespecial',
            name='publicado',
            field=models.BooleanField(default=False, help_text="Indica si l'esdeveniment especial està publicat"),
        ),
    ]
