# Generated by Django 2.0 on 2019-01-23 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0051_auto_20190123_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='setProduct',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]