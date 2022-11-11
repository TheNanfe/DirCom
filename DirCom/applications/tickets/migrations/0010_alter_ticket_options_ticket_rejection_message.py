# Generated by Django 4.1.1 on 2022-11-05 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0009_alter_ticket_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ticket",
            options={"ordering": ["-created_at"], "verbose_name": "ticket"},
        ),
        migrations.AddField(
            model_name="ticket",
            name="rejection_message",
            field=models.TextField(
                blank=True, null=True, verbose_name="motivo del rechazo"
            ),
        ),
    ]
