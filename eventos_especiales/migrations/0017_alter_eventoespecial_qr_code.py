# Generated by Django 4.2.2 on 2023-11-08 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos_especiales', '0016_alter_eventoespecial_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventoespecial',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/', verbose_name='Codi QR'),
        ),
    ]