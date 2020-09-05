# Generated by Django 2.0 on 2019-06-25 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0076_auto_20190531_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcode',
            name='calculation',
            field=models.CharField(choices=[('order', '주문'), ('store', '주문재고'), ('other', '수기')], default='order', max_length=10),
        ),
        migrations.AlterField(
            model_name='productegg',
            name='type',
            field=models.CharField(choices=[('할란', '할란'), ('할란사용', '할란사용'), ('공정품투입', '공정품투입'), ('공정품발생', '공정품발생'), ('공정품폐기', '공정품폐기'), ('미출고품사용', '미출고품사용'), ('미출고품투입', '미출고품투입')], default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='setproductmatch',
            name='setProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]