from email.policy import default
from enum import unique
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models hemok


class Appointment(models.Model):
    APPT_STATUS = (('PENDING', 'pending'), ('SCHEDULED',
                                            'scheduled'), ('REJECTED', 'rejected'),)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    appt_status = models.CharField(
        max_length=10, choices=APPT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recipients = models.IntegerField()
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

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
