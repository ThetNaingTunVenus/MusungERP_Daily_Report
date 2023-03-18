# Generated by Django 4.1.7 on 2023-03-10 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('BuyerName', models.CharField(max_length=225, primary_key=True, serialize=False)),
                ('Address', models.CharField(max_length=225)),
            ],
            options={
                'db_table': 'Buyer',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('ItemName', models.CharField(max_length=225, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Item',
            },
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('Name', models.CharField(max_length=225, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Line',
            },
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('StyleCode', models.CharField(max_length=225, primary_key=True, serialize=False)),
                ('Buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.buyer')),
            ],
            options={
                'db_table': 'Style',
            },
        ),
    ]