# Generated by Django 4.2.2 on 2023-06-22 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0062_alter_post_titulo'),
        ('personalizacion', '0018_carruselsubblog'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeleccionDestacados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(help_text='Escriu un nom únic', max_length=100)),
                ('coleccion', models.ManyToManyField(blank=True, related_name='seleccions', to='blog.post')),
            ],
        ),
    ]
