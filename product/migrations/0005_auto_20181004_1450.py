# Generated by Django 2.0 on 2018-10-04 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20181004_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcode',
            name='price',
            field=models.FloatField(),
        ),
    ]
