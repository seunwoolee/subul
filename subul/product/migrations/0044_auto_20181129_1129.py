# Generated by Django 2.0 on 2018-11-29 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_auto_20181120_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setproductmatch',
            name='setProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
