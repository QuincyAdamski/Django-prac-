# Generated by Django 5.1.6 on 2025-04-07 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theApp', '0007_event_registered_useres'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='registered_useres',
            new_name='registered_users',
        ),
    ]
