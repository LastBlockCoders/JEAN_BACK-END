# Generated by Django 4.1.1 on 2022-10-27 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0015_remove_booking_name_of_service_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='service',
        ),
        migrations.AddField(
            model_name='booking',
            name='service_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
