# Generated by Django 4.2.2 on 2023-11-02 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_utils', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registroerror',
            name='mensaje',
        ),
        migrations.AddField(
            model_name='registroerror',
            name='descripcion',
            field=models.TextField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registroerror',
            name='titulo',
            field=models.TextField(editable=False, null=True),
        ),
    ]
