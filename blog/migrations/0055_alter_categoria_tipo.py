# Generated by Django 4.2.2 on 2023-06-19 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0054_alter_categoria_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='tipo',
            field=models.CharField(choices=[('normal', 'normal'), ('agenda', 'agenda'), ('visitas_guiadas', 'visitas guiadas'), ('noticies', 'noticies')], default='normal', max_length=20),
        ),
    ]
