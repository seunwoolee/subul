# Generated by Django 2.0 on 2018-11-04 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_auto_20181102_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='totalPrice',
        ),
        migrations.AlterField(
            model_name='order',
            name='setProduct',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
