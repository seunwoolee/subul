# Generated by Django 2.0 on 2018-12-03 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0026_auto_20181129_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='setProduct',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
        migrations.AlterField(
            model_name='order',
            name='specialTag',
            field=models.CharField(choices=[('일반', ''), ('특인가', '특인가')], default='일반', max_length=10),
        ),
    ]
