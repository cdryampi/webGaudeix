# Generated by Django 3.2.19 on 2023-06-07 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0046_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='tipo',
            field=models.CharField(choices=[('normal', 'normal'), ('agenda', 'agenda'), ('visitas_guiadas', 'visitas guiadas')], default='normal', max_length=20),
        ),
    ]
