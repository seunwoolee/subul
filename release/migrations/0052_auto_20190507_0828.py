# Generated by Django 2.0 on 2019-05-06 23:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0051_merge_20190328_0846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='release',
            name='delete_state',
        ),
        migrations.AlterField(
            model_name='release',
            name='releaseSetProductCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]