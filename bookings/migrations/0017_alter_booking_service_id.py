# Generated by Django 4.1.1 on 2022-10-27 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_alter_service_name'),
        ('bookings', '0016_remove_booking_service_booking_service_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='service_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service'),
        ),
    ]