# Generated by Django 2.0 on 2018-11-19 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0040_auto_20181114_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productadmin',
            name='releaseType',
            field=models.CharField(choices=[('생성', '생성'), ('판매', '판매'), ('샘플', '샘플'), ('증정', '증정'), ('자손', '자손'), ('반품', '반품'), ('이동', '이동'), ('미출고품', '미출고품'), ('재고조정', '재고조정')], default='생성', max_length=10),
        ),
        migrations.AlterField(
            model_name='setproductmatch',
            name='setProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
