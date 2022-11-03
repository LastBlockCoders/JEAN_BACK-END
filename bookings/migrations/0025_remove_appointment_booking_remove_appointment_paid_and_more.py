# Generated by Django 4.1.1 on 2022-11-03 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_alter_service_status'),
        ('bookings', '0024_delete_appointmentstats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='booking',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='payment_status',
        ),
        migrations.AddField(
            model_name='appointment',
            name='recipients',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='services.service'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appt_status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('SCHEDULE', 'scheduled'), ('DECLINE', 'declined'), ('CANCELLED', 'cancelled'), ('COMPLETED', 'completed'), ('MISSED', 'missed')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='payment_method',
            field=models.CharField(default='Cash', max_length=25),
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
    ]