# Generated by Django 2.0 on 2018-11-05 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0035_auto_20181105_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productadmin',
            name='releaseType',
            field=models.CharField(choices=[('생성', '생성'), ('판매', '판매'), ('샘플', '샘플'), ('증정', '증정'), ('자손', '자손'), ('이동', '이동'), ('반품', '반품')], default='생성', max_length=10),
        ),
        migrations.AlterField(
            model_name='setproductmatch',
            name='setProductCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
