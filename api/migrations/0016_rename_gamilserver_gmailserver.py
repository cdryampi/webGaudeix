# Generated by Django 4.2.2 on 2023-10-31 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_gamilserver_recipient_email_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GamilServer',
            new_name='GmailServer',
        ),
    ]