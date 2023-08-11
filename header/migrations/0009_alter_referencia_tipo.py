# Generated by Django 4.2.2 on 2023-08-10 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0008_headerfooter_referencia_subvencion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referencia',
            name='tipo',
            field=models.CharField(choices=[('post', 'Post'), ('categoria', 'Categoría'), ('subblog', 'SubBlog'), ('externo', 'Enlace Externo'), ('contacto', 'Contacto'), ('evento_especial', 'evento_especial'), ('subvencion', 'Subvencion')], max_length=30),
        ),
    ]