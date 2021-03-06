# Generated by Django 2.0 on 2018-11-06 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0037_auto_20181105_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amount_kg',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='setproductmatch',
            name='setProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
