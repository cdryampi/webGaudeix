# Generated by Django 4.2.2 on 2023-06-19 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0005_alter_mappoint_icono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappoint',
            name='icono',
            field=models.CharField(choices=[('station', 'Estació'), ('restaurant', 'Restaurant'), ('library', 'Biblioteca'), ('hotel', 'Hotel'), ('town-hall', 'Ajuntament'), ('theater', 'Centre Cultural'), ('sport', 'Esports'), ('serveis', 'Serveis'), ('transports', 'Transports'), ('aparcaments', 'Aparcaments'), ('platges', 'Platges'), ('informació', "Punt d'informació"), ('jaciments', 'Jaciments arqueològics')], max_length=100),
        ),
    ]