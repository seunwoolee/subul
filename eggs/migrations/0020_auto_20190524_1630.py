# Generated by Django 2.0 on 2019-05-24 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0019_auto_20190524_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eggorder',
            name='orderMaster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eggs.EggOrderMaster'),
        ),
    ]