# Generated by Django 2.0 on 2019-09-04 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packing', '0011_auto_20190904_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packing',
            name='autoRelease',
        ),
    ]
