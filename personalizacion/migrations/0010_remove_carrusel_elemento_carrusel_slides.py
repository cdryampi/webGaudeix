# Generated by Django 4.2 on 2023-05-25 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalizacion', '0009_remove_carrusel_elementos_carrusel_elemento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrusel',
            name='elemento',
        ),
        migrations.AddField(
            model_name='carrusel',
            name='slides',
            field=models.ManyToManyField(related_name='carruseles', to='personalizacion.slide'),
        ),
    ]