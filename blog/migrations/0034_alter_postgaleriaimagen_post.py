# Generated by Django 4.2 on 2023-05-22 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0033_postfichero_postgaleriaimagen_postimagen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postgaleriaimagen',
            name='post',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]