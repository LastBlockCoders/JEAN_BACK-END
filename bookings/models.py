from email.policy import default
from enum import unique
from django.db import models
from services.models import Service
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models hemok


class AppLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=2000, null=True, blank=True)
    address = models.CharField(max_length=255,  null=True, blank=True)
    city = models.CharField(max_length=255,  null=True, blank=True)
    country = models.CharField(max_length=255,  null=True, blank=True)
    zip_code = models.CharField(max_length=4,  null=True, blank=True)
    longitude = models.CharField(max_length=255,  null=True, blank=True)
    latitude = models.CharField(max_length=255,  null=True, blank=True)


class Booking(models.Model):
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    recipients = models.IntegerField()
    amount = models.IntegerField()


class Appointment(models.Model):
    APPT_STATUS = (('PENDING', 'pending'), ('SCHEDULE',
                                            'scheduled'), ('REJECT', 'rejected'), ('CANCEL', 'cancelled'), ('ACCEPT', 'accepted'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ManyToManyField(Booking)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    appt_status = models.CharField(
        max_length=10, choices=APPT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    total_price = models.IntegerField()
    payment_status = models.CharField(max_length=8, default='UNPAID')
    payment_method = models.CharField(max_length=25, default='EFT-Card')

    class Meta:
        ordering = ["start_date"]

    def schedule(self):
        self.approve = True
        self.status = self.APPT_STATUS[1]

    def get_id(self):
        id = self.get_id()
        return id


class BookedSlot(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    appt_date = models.DateField()
