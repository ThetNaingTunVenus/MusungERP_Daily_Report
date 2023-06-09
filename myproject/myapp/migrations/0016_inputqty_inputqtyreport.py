# Generated by Django 4.1.7 on 2023-03-17 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_alter_dailydata_dailycmpbyline_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputQty',
            fields=[
                ('line', models.CharField(max_length=225)),
                ('style', models.CharField(max_length=225, primary_key=True, serialize=False)),
                ('inputqty', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'InputQty',
            },
        ),
        migrations.CreateModel(
            name='InputQtyReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('line', models.CharField(max_length=225)),
                ('style', models.CharField(max_length=225)),
                ('inputqty', models.IntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'InputQtyReport',
            },
        ),
    ]
