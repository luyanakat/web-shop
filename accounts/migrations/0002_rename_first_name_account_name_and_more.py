# Generated by Django 5.0.1 on 2024-01-19 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='last_name',
        ),
    ]
