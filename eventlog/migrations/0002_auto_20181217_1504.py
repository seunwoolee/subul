# Generated by Django 2.0 on 2018-12-17 06:04

from django.db import migrations
import eventlog.models


class Migration(migrations.Migration):

    dependencies = [
        ('eventlog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='extra',
            field=eventlog.models.UTF8JSONField(),
        ),
    ]
