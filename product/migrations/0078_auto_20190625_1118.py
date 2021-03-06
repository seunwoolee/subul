# Generated by Django 2.0 on 2019-06-25 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_location_location_owner'),
        ('product', '0077_auto_20190625_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ymd', models.CharField(max_length=8)),
                ('code', models.CharField(max_length=255)),
                ('codeName', models.CharField(max_length=255)),
                ('count', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('amount_kg', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=19, null=True)),
                ('memo', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('전란', '전란'), ('난백난황', '난백난황')], default='전란', max_length=30)),
                ('productCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductCode')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductOrderPacking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderLocationCodeName', models.CharField(max_length=255)),
                ('boxCount', models.IntegerField()),
                ('eaCount', models.IntegerField()),
                ('orderLocationCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Location')),
                ('productOrderCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductOrder')),
            ],
        ),
        migrations.AlterField(
            model_name='setproductmatch',
            name='setProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
