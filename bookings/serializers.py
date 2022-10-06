import pytz
from datetime import datetime, timedelta, time
from email.policy import default
from rest_framework import serializers
from .models import Appointment, BookedSlot
from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError
User = get_user_model()


class BookingSerializer(serializers.ModelSerializer):
    recipients = serializers.IntegerField(write_only=True)
    start_date = serializers.DateField(required=True)
    start_time = serializers.TimeField(required=True)
    end_time = serializers.TimeField(required=True)
    appt_status = serializers.HiddenField(default='pending')
    approved = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True,
                                           default=serializers.CreateOnlyDefault(datetime.now()))
    updated_at = serializers.DateTimeField(
        read_only=True, default=datetime.now())

    class Meta:
        model = Appointment
        fields = ["id", "recipients", "start_date", "start_time", "end_time",
                  "appt_status", "approved", "created_at", "updated_at"]

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user

    def validate(self, attrs):
        sdate = attrs["start_date"]
        start_time = attrs["start_time"]
        recipients = attrs["recipients"]
        start_time = datetime.combine(sdate, start_time)
        # I will get this from the service duration
        end_time = start_time + timedelta(minutes=10)
        # The hours an appoitment should not exceed
        over_time = start_time + timedelta(hours=5)

        today = datetime.now()
        time_now = today
        startDate_passed = pytz.utc.localize(
            today).date() > sdate and time_now > start_time

        if startDate_passed:
            raise ValidationError("booking date/time has passed")

        elif end_time < start_time or end_time > over_time:
            raise ValidationError("appointment duration is too long")

        if recipients > 10:
            raise ValidationError("recipients exceed ten people")

        booked_appts = BookedSlot.objects.filter(appt_date=sdate)
        if booked_appts.exists():
            for appt in booked_appts:
                if start_time > datetime.combine(appt.appt_date, appt.start_time) and end_time < datetime.combine(appt.appt_date, appt.end_time):
                    raise ValidationError(
                        "appointment slot already booked")

                if start_time < datetime.combine(appt.appt_date, appt.start_time) and end_time > datetime.combine(appt.appt_date, appt.end_time):
                    raise ValidationError(
                        "appointment slot already booked")
                if start_time < datetime.combine(appt.appt_date, appt.end_time) and end_time > datetime.combine(appt.appt_date, appt.end_time):
                    raise ValidationError(
                        "appointment slot already booked")

        return super().validate(attrs)

    def create(self, validated_data):

        booking = super().create(validated_data)

        booking.save()

        return booking


class BookingDetailsSerializer(serializers.ModelSerializer):
    recipients = serializers.IntegerField()
    start_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    approved = serializers.BooleanField(read_only=True)
    appt_status = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    class Meta:
        model = Appointment
        fields = ["id", "recipients", "start_date", "start_time", "end_time", "approved",
                  "appt_status", "created_at", "updated_at"]


class BookingUpdateStatusSerializer(serializers.ModelSerializer):
    appt_status = serializers.CharField()
    approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = Appointment
        fields = ["appt_status", "approved", ]


class BookedSlotListSerializer(serializers.ModelSerializer):
    appt_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    class Meta:
        model = BookedSlot
        fields = ["id", "appointment", "appt_date", "start_time", "end_time"]
