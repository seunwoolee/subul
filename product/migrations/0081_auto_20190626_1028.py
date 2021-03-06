# Generated by Django 2.0 on 2019-06-26 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0080_auto_20190626_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorderpacking',
            name='productOrderCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='product.ProductOrder'),
        ),
        migrations.AlterField(
            model_name='setproductmatch',
            name='setProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
