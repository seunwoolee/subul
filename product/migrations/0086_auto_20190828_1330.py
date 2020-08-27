# Generated by Django 2.0 on 2019-08-28 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0085_auto_20190828_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='productorder',
            name='future_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='future', to='product.ProductOrder', verbose_name='차주재고'),
        ),
        migrations.AddField(
            model_name='productorder',
            name='past_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='past', to='product.ProductOrder', verbose_name='전주재고'),
        ),
        migrations.AlterField(
            model_name='productorderpacking',
            name='boxCount',
            field=models.IntegerField(verbose_name='박스수'),
        ),
        migrations.AlterField(
            model_name='productorderpacking',
            name='eaCount',
            field=models.IntegerField(verbose_name='낱개수'),
        ),
        migrations.AlterField(
            model_name='productorderpacking',
            name='future_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='future', to='product.ProductOrderPacking', verbose_name='차주재고'),
        ),
        migrations.AlterField(
            model_name='productorderpacking',
            name='orderLocationCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Location', verbose_name='주문장소'),
        ),
        migrations.AlterField(
            model_name='productorderpacking',
            name='orderLocationCodeName',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='주문장소명'),
        ),
        migrations.AlterField(
            model_name='productorderpacking',
            name='past_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='past', to='product.ProductOrderPacking', verbose_name='전주재고'),
        ),
        migrations.AlterField(
            model_name='productorderpacking',
            name='productOrderCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='product.ProductOrder', verbose_name='제품코드'),
        ),
        migrations.AlterField(
            model_name='setproductmatch',
            name='setProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
