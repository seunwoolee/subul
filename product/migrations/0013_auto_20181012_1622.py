# Generated by Django 2.0 on 2018-10-12 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20181010_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productegg',
            name='tank',
        ),
        migrations.AddField(
            model_name='productegg',
            name='code',
            field=models.CharField(default='01201', max_length=10),
        ),
        migrations.AddField(
            model_name='productegg',
            name='codeName',
            field=models.CharField(default='RAW Tank 전란', max_length=255),
        ),
    ]