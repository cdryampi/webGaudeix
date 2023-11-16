# Generated by Django 4.2.2 on 2023-11-15 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalizacion', '0043_alter_superdestacado_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internallink',
            name='categoria',
        ),
        migrations.RemoveField(
            model_name='internallink',
            name='post',
        ),
        migrations.RemoveField(
            model_name='internallink',
            name='subblog',
        ),
        migrations.AlterField(
            model_name='internallink',
            name='tipo',
            field=models.CharField(choices=[('eventos_especiales', 'Esdeveniments especials'), ('compra_y_descubre', 'Compra i descobreix')], max_length=20, verbose_name='Tipus'),
        ),
    ]
