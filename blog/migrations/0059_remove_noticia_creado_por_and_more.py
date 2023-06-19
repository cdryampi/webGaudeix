# Generated by Django 4.2.2 on 2023-06-19 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0058_alter_noticia_categoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noticia',
            name='creado_por',
        ),
        migrations.RemoveField(
            model_name='noticia',
            name='fecha_creacion',
        ),
        migrations.RemoveField(
            model_name='noticia',
            name='fecha_modificacion',
        ),
        migrations.RemoveField(
            model_name='noticia',
            name='modificado_por',
        ),
        migrations.AddField(
            model_name='noticia',
            name='slug',
            field=models.SlugField(default=None, editable=False, unique=True),
            preserve_default=False,
        ),
    ]
