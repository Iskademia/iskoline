# Generated by Django 3.2.9 on 2022-04-27 21:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0016_announcement'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Announcement',
            new_name='AnnouncementPost',
        ),
    ]