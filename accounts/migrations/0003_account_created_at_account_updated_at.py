# Generated by Django 5.0.1 on 2024-01-19 08:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_first_name_account_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 1, 19, 8, 19, 59, 677965, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
