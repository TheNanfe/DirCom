# Generated by Django 4.1.1 on 2022-11-17 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_rename_user_id_notification_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='url_path',
            new_name='url_args',
        ),
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(default='test', max_length=100),
            preserve_default=False,
        ),
    ]