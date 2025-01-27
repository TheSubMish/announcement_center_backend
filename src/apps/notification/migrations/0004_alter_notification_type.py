# Generated by Django 5.0.4 on 2024-12-21 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_notification_announcement_notification_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('group_join', 'Group Join'), ('group_leave', 'Group Leave'), ('group_rate', 'Group Rate'), ('announcement_create', 'Announcement Create'), ('announcement_update', 'Announcement Update'), ('announcement_comment_create', 'Announcement Comment Create'), ('announcement_like', 'Announcement Like'), ('announcement_unlike', 'Announcement Unlike')], default='group_join', max_length=100),
        ),
    ]
