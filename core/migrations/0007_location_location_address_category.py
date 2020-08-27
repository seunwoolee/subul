from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_location_location_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='location_address_category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
