# Generated by Django 4.2.2 on 2023-08-07 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos_especiales', '0004_eventoespecial_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventoespecial',
            name='logo_especial',
            field=models.ImageField(blank=True, help_text="Logotip especial per a l'esdeveniment", null=True, upload_to='eventos_especiales/'),
        ),
    ]