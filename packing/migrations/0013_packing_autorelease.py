# Generated by Django 2.0 on 2019-09-04 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packing', '0012_remove_packing_autorelease'),
    ]

    operations = [
        migrations.AddField(
            model_name='packing',
            name='autoRelease',
            field=models.CharField(blank=True, choices=[('자동출고', '자동출고'), ('수동출고', '수동출고')], max_length=10, null=True),
        ),
    ]