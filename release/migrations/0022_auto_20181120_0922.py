# Generated by Django 2.0 on 2018-11-20 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0021_auto_20181120_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='releaseSetProductCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
        migrations.AlterField(
            model_name='release',
            name='specialTag',
            field=models.CharField(choices=[('일반', '일반'), ('특인가', '특인가')], default='', max_length=10),
        ),
    ]
