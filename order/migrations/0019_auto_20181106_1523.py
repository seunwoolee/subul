# Generated by Django 2.0 on 2018-11-06 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_auto_20181105_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount_kg',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='setProduct',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
