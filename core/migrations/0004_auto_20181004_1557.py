# Generated by Django 2.0 on 2018-10-04 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20181002_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location_address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='location',
            name='location_companyNumber',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='location',
            name='location_phone',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
