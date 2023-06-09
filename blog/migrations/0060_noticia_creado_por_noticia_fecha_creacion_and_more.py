# Generated by Django 4.2.2 on 2023-06-19 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0059_remove_noticia_creado_por_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticia',
            name='creado_por',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_creados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='noticia',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Data de creació'),
        ),
        migrations.AddField(
            model_name='noticia',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True, help_text='Data de modificació'),
        ),
        migrations.AddField(
            model_name='noticia',
            name='modificado_por',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
