# Generated by Django 4.2.2 on 2024-04-18 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personalizacion', '0075_alter_personalizacion_alerta'),
    ]

    operations = [
        migrations.AddField(
            model_name='superdestacado',
            name='flyer',
            field=models.ImageField(blank=True, help_text="Puja el flyer de l'esdeveniment en format DIN A3", null=True, upload_to='personalizacion/flyers/', verbose_name='Flyer'),
        ),
        migrations.AddField(
            model_name='superdestacado',
            name='link_generico',
            field=models.URLField(blank=True, help_text='Enllaç oblogatori quan no tenim viculat un descatat viculat.', null=True),
        ),
        migrations.AlterField(
            model_name='superdestacado',
            name='destacado',
            field=models.OneToOneField(blank=True, help_text='Selecciona un enllaç intern per fer la vinculació', null=True, on_delete=django.db.models.deletion.CASCADE, to='personalizacion.internallink', verbose_name='Destacat'),
        ),
    ]
