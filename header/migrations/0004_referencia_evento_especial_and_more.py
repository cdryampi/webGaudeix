# Generated by Django 4.2.2 on 2023-07-07 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventos_especiales', '0002_eventoespecial_publicado'),
        ('header', '0003_referencia_contacto_alter_referencia_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='referencia',
            name='evento_especial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='eventos_especiales.eventoespecial'),
        ),
        migrations.AlterField(
            model_name='enlaceexterno',
            name='titulo',
            field=models.CharField(help_text="Títol de l'enllaç", max_length=35),
        ),
        migrations.AlterField(
            model_name='referencia',
            name='tipo',
            field=models.CharField(choices=[('post', 'Post'), ('categoria', 'Categoría'), ('subblog', 'SubBlog'), ('externo', 'Enlace Externo'), ('contacto', 'Contacto'), ('evento_especial', 'evento_especial')], max_length=30),
        ),
    ]
