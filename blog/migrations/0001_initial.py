# Generated by Django 4.2.1 on 2023-05-15 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(help_text='Título del subblog', max_length=100)),
                ('slug', models.SlugField(help_text='Slug del subblog', unique=True)),
                ('contenido', models.TextField(help_text='Contenido del subblog')),
                ('imagen', models.ImageField(help_text='Imagen del subblog', upload_to='blog/subblogs/')),
                ('color', models.CharField(help_text='Color en formato hexadecimal (ejemplo: #FF0000)', max_length=7)),
                ('link', models.CharField(help_text='Enlace del subblog', max_length=200)),
                ('abrir_en_nueva_ventana', models.BooleanField(default=False, help_text='Abrir enlace en una nueva ventana')),
                ('abrir_en_pespana', models.BooleanField(default=False, help_text="Abrir enlace en la misma ventana con rel='noopener noreferrer'")),
                ('metatitulo', models.CharField(help_text='Metatítulo para SEO', max_length=255)),
                ('metadescripcion', models.TextField(help_text='Metadescripción para SEO')),
            ],
        ),
    ]
