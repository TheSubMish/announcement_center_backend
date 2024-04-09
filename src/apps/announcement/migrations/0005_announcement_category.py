# Generated by Django 5.0.2 on 2024-04-09 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0004_announcement_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='category',
            field=models.CharField(choices=[('web', 'Web'), ('network', 'Network'), ('cyber', 'Cyber'), ('cloud', 'Cloud'), ('art', 'Art'), ('food', 'Food'), ('entertainment', 'Entertainment'), ('health', 'Health'), ('lifestyle', 'Lifestyle'), ('sports', 'Sports'), ('travel', 'Travel'), ('other', 'Other')], default='web', max_length=100),
        ),
    ]
