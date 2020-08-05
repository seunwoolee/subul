# Generated by Django 2.0 on 2019-06-10 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0023_auto_20190531_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='eggorder',
            name='site_memo',
            field=models.TextField(blank=True, null=True, verbose_name='현장메모'),
        ),
        migrations.AlterField(
            model_name='eggorder',
            name='code',
            field=models.CharField(max_length=255, verbose_name='코드'),
        ),
        migrations.AlterField(
            model_name='eggorder',
            name='codeName',
            field=models.CharField(max_length=255, verbose_name='코드명'),
        ),
        migrations.AlterField(
            model_name='eggorder',
            name='in_locationCodeName',
            field=models.CharField(max_length=255, verbose_name='입고처명'),
        ),
        migrations.AlterField(
            model_name='eggorder',
            name='in_ymd',
            field=models.CharField(max_length=8, verbose_name='입고일'),
        ),
        migrations.AlterField(
            model_name='eggorder',
            name='memo',
            field=models.TextField(blank=True, null=True, verbose_name='지시자메모'),
        ),
        migrations.AlterField(
            model_name='eggorder',
            name='orderCount',
            field=models.IntegerField(verbose_name='지시량'),
        ),
        migrations.AlterField(
            model_name='eggorder',
            name='ymd',
            field=models.CharField(max_length=8, verbose_name='날짜'),
        ),
    ]
