# Generated by Django 2.0 on 2019-01-22 04:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0061_auto_20190122_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='product',
            name='amount_kg',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=19, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='loss_clean',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='product',
            name='loss_fill',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='productadmin',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='productcode',
            name='amount_kg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='total_loss_clean',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='total_loss_fill',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='total_loss_insert',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='total_loss_openEgg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='setproductmatch',
            name='setProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
