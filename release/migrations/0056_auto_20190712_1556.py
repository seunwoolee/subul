# Generated by Django 2.0 on 2019-07-12 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0055_auto_20190701_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='releaseSetProductCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
