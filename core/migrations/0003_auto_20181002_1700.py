# Generated by Django 2.0 on 2018-10-02 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20181002_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='type',
            field=models.CharField(choices=[('01', '포장재입고'), ('03', '원란입고'), ('05', '판매'), ('07', '원란판매'), ('09', 'OEM입고거래처')], default='05', max_length=2),
        ),
    ]
