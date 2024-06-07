# Generated by Django 5.0.4 on 2024-06-07 05:09

import django.db.models.deletion
import django.utils.timezone
import src.apps.common.utills
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'InActive')], default='active', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('profilepic', models.ImageField(blank=True, null=True, upload_to='profile', validators=[src.apps.common.utills.image_validate])),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('terms', models.BooleanField(default=True)),
                ('otp', models.CharField(blank=True, max_length=10, null=True)),
                ('otp_tries', models.IntegerField(default=0)),
                ('otp_created_at', models.DateTimeField(blank=True, null=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'InActive')], default='active', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('device_ip', models.CharField(max_length=100)),
                ('device_type', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('coordinates', models.CharField(blank=True, max_length=50, null=True)),
                ('device_os', models.CharField(max_length=50)),
                ('browser_type', models.CharField(max_length=50)),
                ('access_token', models.CharField(max_length=650)),
                ('refresh_token', models.CharField(max_length=650)),
                ('is_active', models.BooleanField(default=True)),
                ('blacklist_ip', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
