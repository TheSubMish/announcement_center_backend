# Generated by Django 5.0.4 on 2024-12-10 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_grouppayment_amount_grouppayment_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouppayment',
            name='recurring_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
