# Generated by Django 5.0.4 on 2024-12-21 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_announcementgroup_click_through'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmember',
            name='flagged',
            field=models.BooleanField(default=False),
        ),
    ]