# Generated by Django 5.0.4 on 2024-06-05 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0006_remove_announcementgroup_admin_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcementgroup',
            name='group_type',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='public', max_length=100),
        ),
        migrations.AddField(
            model_name='announcementgroup',
            name='invite_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
