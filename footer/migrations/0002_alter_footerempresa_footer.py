# Generated by Django 4.2.2 on 2024-02-15 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('footer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footerempresa',
            name='footer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresas', to='footer.footer'),
        ),
    ]
