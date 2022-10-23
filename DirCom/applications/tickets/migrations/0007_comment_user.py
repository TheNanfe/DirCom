# Generated by Django 4.1.1 on 2022-10-23 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tickets", "0006_alter_comment_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_comments",
                to=settings.AUTH_USER_MODEL,
                verbose_name="autor",
            ),
            preserve_default=False,
        ),
    ]
