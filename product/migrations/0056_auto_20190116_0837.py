# Generated by Django 2.0 on 2019-01-15 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0055_auto_20190115_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setproductmatch',
            name='setProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
