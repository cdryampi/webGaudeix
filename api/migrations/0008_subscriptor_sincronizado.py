# Generated by Django 4.2.2 on 2023-06-15 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_subscriptor_teenvio'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptor',
            name='sincronizado',
            field=models.BooleanField(default=False),
        ),
    ]
