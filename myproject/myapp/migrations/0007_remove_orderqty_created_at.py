# Generated by Django 4.1.7 on 2023-03-13 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_orderqty_order_qty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderqty',
            name='created_at',
        ),
    ]
