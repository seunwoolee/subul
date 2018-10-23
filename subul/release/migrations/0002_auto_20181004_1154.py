# Generated by Django 2.0 on 2018-10-04 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20181004_1043'),
        ('release', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='product_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='product', to='product.ProductAdmin'),
        ),
        migrations.AlterField(
            model_name='release',
            name='releaseOrder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order'),
        ),
        migrations.AlterField(
            model_name='release',
            name='releaseSetProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]