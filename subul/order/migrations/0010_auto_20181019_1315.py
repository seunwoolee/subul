# Generated by Django 2.0 on 2018-10-19 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20181019_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='memo',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='setProduct',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
