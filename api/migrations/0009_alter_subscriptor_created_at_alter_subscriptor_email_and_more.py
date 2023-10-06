# Generated by Django 4.2.2 on 2023-10-06 06:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_subscriptor_sincronizado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptor',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Dada de donació.', verbose_name="Donat d'alta"),
        ),
        migrations.AlterField(
            model_name='subscriptor',
            name='email',
            field=models.EmailField(help_text='Correu electrònic del subscriptor', max_length=254, verbose_name='Correu electrònic'),
        ),
        migrations.AlterField(
            model_name='subscriptor',
            name='exportable',
            field=models.BooleanField(default=True, help_text='El subscriptor és exportable?', verbose_name='exportable'),
        ),
        migrations.AlterField(
            model_name='subscriptor',
            name='name',
            field=models.CharField(help_text='Nom del subscriptor', max_length=100, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='subscriptor',
            name='sincronizado',
            field=models.BooleanField(default=False, help_text='El subscriptor està sincronitzat?', verbose_name='sincronitzat'),
        ),
        migrations.AlterField(
            model_name='teenvio',
            name='action',
            field=models.CharField(choices=[('contact_save', 'Guardar contacto')], default='contact_save', help_text='Acció per defecte', max_length=20, verbose_name='Acció'),
        ),
        migrations.AlterField(
            model_name='teenvio',
            name='password',
            field=models.CharField(help_text='Contraseña de Teenvio', max_length=100, verbose_name='contrasenya'),
        ),
        migrations.AlterField(
            model_name='teenvio',
            name='plan',
            field=models.CharField(help_text='Plan de Teenvio', max_length=100, verbose_name='Pla'),
        ),
        migrations.AlterField(
            model_name='teenvio',
            name='url',
            field=models.URLField(default='https://master5.teenvio.com/v4/public/api/v3/post/', help_text='URL de la API de Teenvio', verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='teenvio',
            name='user',
            field=models.CharField(help_text='Nombre de usuario de Teenvio', max_length=100, verbose_name="Nom d'usuari de Teenvio"),
        ),
    ]
