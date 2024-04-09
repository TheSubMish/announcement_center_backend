# Generated by Django 5.0.4 on 2024-04-08 07:21

import src.apps.common.utills
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'InActive')], default='active', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(default='', upload_to='announcement', validators=[src.apps.common.utills.image_validate])),
                ('paid_for_email', models.BooleanField(default=True)),
                ('paid_amount', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
