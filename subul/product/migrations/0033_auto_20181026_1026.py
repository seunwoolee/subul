# Generated by Django 2.0 on 2018-10-26 01:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0032_auto_20181025_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='productadmin',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='productegg',
            name='pastTank_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='productegg',
            name='rawTank_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='total_eggUse',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='total_loss_clean',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='total_loss_fill',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='total_loss_insert',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='total_loss_openEgg',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='total_openEgg',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='total_produceStore',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='total_productAmount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='total_storeInsert',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='setproductmatch',
            name='setProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
