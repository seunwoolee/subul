# Generated by Django 2.0 on 2019-05-06 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0017_eggcode_sorts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='egg',
            name='delete_state',
        ),
    ]