# Generated by Django 2.0 on 2019-06-28 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0081_auto_20190626_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorderpacking',
            name='orderLocationCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Location'),
        ),
        migrations.AlterField(
            model_name='productorderpacking',
            name='orderLocationCodeName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='setproductmatch',
            name='setProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]