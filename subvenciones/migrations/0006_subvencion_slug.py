# Generated by Django 4.2.2 on 2023-08-11 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subvenciones', '0005_alter_subvencion_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='subvencion',
            name='slug',
            field=models.SlugField(default=1, editable=False, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]