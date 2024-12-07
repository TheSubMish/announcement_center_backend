# Generated by Django 5.0.4 on 2024-12-07 12:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('group_join', 'Group Join'), ('group_leave', 'Group Leave'), ('announcement_create', 'Announcement Create'), ('announcement_update', 'Announcement Update'), ('announcement_comment_create', 'Announcement Comment Create'), ('announcement_like', 'Announcement Like'), ('announcement_unlike', 'Announcement Unlike')], default='group_join', max_length=100)),
                ('message', models.CharField(max_length=255)),
                ('read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
