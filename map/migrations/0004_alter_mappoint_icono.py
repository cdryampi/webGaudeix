# Generated by Django 4.2.2 on 2023-06-19 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_mappoint_publicado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappoint',
            name='icono',
            field=models.CharField(choices=[('station', 'Estació'), ('restaurant', 'Restaurant'), ('library', 'Biblioteca'), ('hotel', 'Hotel'), ('town-hall', 'Ajuntament'), ('theater', 'Centre Cultural'), ('sport', 'Esports'), ('serveis', 'Serveis'), ('transports', 'Transports'), ('aparcaments', 'Aparcaments'), ('platges', 'Platges')], max_length=100),
        ),
    ]
