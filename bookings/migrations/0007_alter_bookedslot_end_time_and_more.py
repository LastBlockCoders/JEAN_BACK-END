# Generated by Django 4.1.1 on 2022-10-05 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_appointment_start_date_bookedslot_appt_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedslot',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='bookedslot',
            name='start_time',
            field=models.TimeField(),
        ),
    ]
