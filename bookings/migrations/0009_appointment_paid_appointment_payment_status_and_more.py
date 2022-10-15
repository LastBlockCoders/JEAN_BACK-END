# Generated by Django 4.1.1 on 2022-10-11 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
        ('bookings', '0008_alter_appointment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='appointment',
            name='payment_status',
            field=models.CharField(default='UNPAID', max_length=8),
        ),
        migrations.AddField(
            model_name='appointment',
            name='service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='services.service'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appt_status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('SCHEDULE', 'scheduled'), ('REJECT', 'rejected'), ('CANCEL', 'cancelled'), ('ACCEPT', 'accepted')], default='pending', max_length=10),
        ),
    ]
