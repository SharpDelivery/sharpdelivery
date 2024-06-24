# Generated by Django 3.2.1 on 2024-06-24 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='delivery_address',
        ),
        migrations.AddField(
            model_name='customer',
            name='ip_address',
            field=models.GenericIPAddressField(default='127.0.0.1'),
        ),
    ]
