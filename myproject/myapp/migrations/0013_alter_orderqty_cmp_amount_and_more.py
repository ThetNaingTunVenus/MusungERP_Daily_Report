# Generated by Django 4.1.7 on 2023-03-14 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_remove_orderqty_line_remove_orderqtyreport_line_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderqty',
            name='cmp_amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='orderqtyreport',
            name='cmp_amount',
            field=models.FloatField(),
        ),
    ]