# Generated by Django 2.0 on 2019-01-22 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0035_auto_20190118_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='releaseSetProductCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]