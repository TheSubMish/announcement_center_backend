# Generated by Django 5.0.4 on 2024-12-10 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcementgroup',
            name='click_through',
            field=models.IntegerField(default=0),
        ),
    ]
