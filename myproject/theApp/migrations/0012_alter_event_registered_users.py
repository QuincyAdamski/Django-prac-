# Generated by Django 5.1.6 on 2025-04-20 21:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theApp', '0011_remove_event_date_course_end_time_course_start_time_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='registered_users',
            field=models.ManyToManyField(blank=True, related_name='registered_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
