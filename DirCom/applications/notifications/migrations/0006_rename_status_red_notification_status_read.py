# Generated by Django 4.1.1 on 2022-11-17 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_alter_notification_status_red'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='status_red',
            new_name='status_read',
        ),
    ]