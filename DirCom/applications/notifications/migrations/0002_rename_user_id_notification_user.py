# Generated by Django 4.1.1 on 2022-11-14 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='user_id',
            new_name='user',
        ),
    ]
