# Generated by Django 4.1.7 on 2023-03-17 06:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_inputqty_inputqtyreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputqtyreport',
            name='create_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inputqtyreport',
            name='date',
            field=models.DateField(),
        ),
    ]