# Generated by Django 2.0 on 2019-11-18 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0062_auto_20191114_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlist',
            name='car',
        ),
        migrations.AlterField(
            model_name='release',
            name='releaseSetProductCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
