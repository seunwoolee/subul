# Generated by Django 2.0 on 2019-06-10 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0024_auto_20190610_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='eggorder',
            name='display_state',
            field=models.CharField(choices=[('Y', '보여줌'), ('N', '안보여줌')], default='Y', max_length=10),
        ),
    ]
