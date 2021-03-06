# Generated by Django 2.0 on 2018-10-10 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_auto_20181010_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productadmin',
            name='releaseSeq',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='release.Release'),
        ),
        migrations.AlterField(
            model_name='productadmin',
            name='releaseType',
            field=models.CharField(choices=[('생성', '생성'), ('판매', '판매'), ('샘플', '샘플'), ('증정', '증정'), ('자손', '자손'), ('이동', '이동')], default='생성', max_length=10),
        ),
    ]
