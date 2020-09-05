# Generated by Django 2.0 on 2019-09-04 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0091_auto_20190904_1718'),
        ('packing', '0010_auto_20190123_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoPacking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('packingCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='packing.PackingCode')),
                ('productCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='product.ProductCode')),
            ],
        ),
        migrations.RemoveField(
            model_name='packing',
            name='delete_state',
        ),
        migrations.AddField(
            model_name='packing',
            name='autoRelease',
            field=models.CharField(blank=True, choices=[('자동출고', '자동출고'), ('수동출고', '수동출고')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='packing',
            name='productCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='product.Product'),
        ),
    ]