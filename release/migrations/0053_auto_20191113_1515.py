# Generated by Django 2.0 on 2019-11-13 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_location_location_owner'),
        ('release', '0052_auto_20191113_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('box', models.PositiveIntegerField()),
                ('ea', models.PositiveIntegerField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_list', to='release.Car')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Location')),
                ('pallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_list', to='release.Pallet')),
            ],
        ),
        migrations.AlterField(
            model_name='release',
            name='releaseSetProductCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.SetProductCode'),
        ),
    ]
