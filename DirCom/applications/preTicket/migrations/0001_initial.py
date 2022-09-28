# Generated by Django 4.1.1 on 2022-09-26 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PreTicket',
            fields=[
                ('pre_ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('status', models.CharField(max_length=30)),
                ('subject', models.CharField(max_length=150)),
                ('form_type', models.CharField(max_length=50)),
                ('files', models.FileField(upload_to='')),
            ],
        ),
    ]
