# Generated by Django 3.2.1 on 2024-06-28 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_deliveryorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryorder',
            name='id',
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='tracking_number',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
