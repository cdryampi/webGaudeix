# Generated by Django 4.2.2 on 2023-06-19 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0057_alter_noticia_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.categoria'),
        ),
    ]
