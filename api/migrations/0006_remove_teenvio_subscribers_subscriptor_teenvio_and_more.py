# Generated by Django 4.2.2 on 2023-06-14 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_subscriptor_exportable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teenvio',
            name='subscribers',
        ),
        migrations.AddField(
            model_name='subscriptor',
            name='teenvio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscribers', to='api.teenvio'),
        ),
        migrations.AddField(
            model_name='teenvio',
            name='action',
            field=models.CharField(choices=[('contact_save', 'Guardar contacto')], default='contact_save', help_text='Acción por defecto', max_length=20),
        ),
        migrations.AlterField(
            model_name='teenvio',
            name='gid',
            field=models.CharField(help_text='Identificador de Teenvio', max_length=100),
        ),
        migrations.AlterField(
            model_name='teenvio',
            name='password',
            field=models.CharField(help_text='Contraseña de Teenvio', max_length=100),
        ),
        migrations.AlterField(
            model_name='teenvio',
            name='plan',
            field=models.CharField(help_text='Plan de Teenvio', max_length=100),
        ),
        migrations.AlterField(
            model_name='teenvio',
            name='url',
            field=models.URLField(default='https://master5.teenvio.com/v4/public/api/v3/post/', help_text='URL de la API de Teenvio'),
        ),
        migrations.AlterField(
            model_name='teenvio',
            name='user',
            field=models.CharField(help_text='Nombre de usuario de Teenvio', max_length=100),
        ),
    ]