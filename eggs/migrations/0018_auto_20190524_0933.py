# Generated by Django 2.0 on 2019-05-24 00:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_location_location_owner'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eggs', '0017_eggcode_sorts'),
    ]

    operations = [
        migrations.CreateModel(
            name='EggOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ymd', models.CharField(max_length=8)),
                ('code', models.CharField(max_length=255)),
                ('codeName', models.CharField(max_length=255)),
                ('orderCount', models.IntegerField()),
                ('realCount', models.IntegerField()),
                ('memo', models.TextField(blank=True, null=True)),
                ('priority', models.PositiveIntegerField()),
                ('in_ymd', models.CharField(max_length=8)),
                ('in_locationCodeName', models.CharField(max_length=255)),
                ('commander', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('eggCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='eggs.EggCode')),
                ('in_locationCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Location')),
            ],
        ),
    ]
