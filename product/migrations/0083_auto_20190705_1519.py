# Generated by Django 2.0 on 2019-07-05 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0082_auto_20190628_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcode',
            name='calculation',
            field=models.CharField(choices=[('order', '주문'), ('manual', '수기')], default='order', max_length=10),
        ),
        migrations.AlterField(
            model_name='setproductmatch',
            name='setProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
