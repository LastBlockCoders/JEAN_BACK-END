# Generated by Django 4.1.1 on 2022-10-27 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0017_alter_booking_service_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='total_amount',
            new_name='amount',
        ),
        migrations.AlterField(
            model_name='booking',
            name='service_id',
            field=models.CharField(max_length=255),
        ),
    ]