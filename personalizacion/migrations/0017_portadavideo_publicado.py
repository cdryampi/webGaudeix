# Generated by Django 3.2.19 on 2023-06-05 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalizacion', '0016_videosportada_orden'),
    ]

    operations = [
        migrations.AddField(
            model_name='portadavideo',
            name='publicado',
            field=models.BooleanField(default=False),
        ),
    ]