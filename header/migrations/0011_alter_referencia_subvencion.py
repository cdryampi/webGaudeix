# Generated by Django 4.2.2 on 2023-08-10 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0010_referencia_header_footer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referencia',
            name='subvencion',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
