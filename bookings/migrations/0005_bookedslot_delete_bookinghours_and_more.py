# Generated by Django 4.1.1 on 2022-10-01 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_alter_appointment_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookedSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(db_index=True, unique=True)),
                ('end_time', models.DateTimeField(db_index=True, unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name='BookingHours',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='status',
        ),
        migrations.AddField(
            model_name='appointment',
            name='appt_status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('SCHEDULED', 'scheduled'), ('REJECTED', 'rejected')], default='pending', max_length=10),
        ),
        migrations.DeleteModel(
            name='TimeSlot',
        ),
        migrations.AddField(
            model_name='bookedslot',
            name='appointment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bookings.appointment'),
        ),
    ]
