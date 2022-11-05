from rest_framework.fields import CurrentUserDefault
from urllib import request
import pytz
from datetime import datetime, timedelta
from email.policy import default
from rest_framework import serializers
from .models import Appointment, BookedSlot, AppLocation
from services.models import Service
from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError

User = get_user_model()


class ViewLocationSerializer(serializers.ModelSerializer):
    street = serializers.CharField()
    surburb = serializers.CharField()
    city = serializers.CharField()
    zip_code = serializers.CharField()
    country = serializers.CharField()

    class Meta:
        model = AppLocation
        fields = ['street', 'city', 'surburb', 'zip_code', 'country']


class BookingSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(required=True)
    recipients = serializers.IntegerField()
    start_time = serializers.TimeField(required=True)
    end_time = serializers.TimeField(required=True)
    appt_status = serializers.CharField(read_only=True, default='pending')
    approved = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True,
                                           default=serializers.CreateOnlyDefault(datetime.now()))
    updated_at = serializers.DateTimeField(
        read_only=True, default=datetime.now())
    total_price = serializers.IntegerField(),
    payment_method = serializers.CharField(default='Cash')

    class Meta:
        model = Appointment
        fields = ["start_date", "start_time", "end_time", "recipients",
                  "appt_status", "approved", "created_at", "updated_at", "total_price", "payment_method"]

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user

    def validate(self, attrs):
        sdate = attrs["start_date"]
        start_time = attrs["start_time"]
        end_time = attrs["end_time"]
        start_time = datetime.combine(sdate, start_time)
        end_time = datetime.combine(sdate, end_time)
        # Add 30 min for break in between appointments
        #end_time = end_time + timedelta(minutes=30)
        # The hours an appoitment should not exceed
        over_time = start_time + timedelta(hours=5)

        today = datetime.now()
        time_now = today
        startDate_passed = pytz.utc.localize(
            today).date() > sdate and time_now > start_time

        if startDate_passed:
            raise ValidationError("booking date/time has passed")

        booked_appts = BookedSlot.objects.filter(appt_date=sdate)
        if booked_appts.exists():
            for appt in booked_appts:
                if start_time > datetime.combine(appt.appt_date, appt.start_time) and end_time < datetime.combine(appt.appt_date, appt.end_time):
                    raise ValidationError(
                        "unavailable time slot")

                if start_time < datetime.combine(appt.appt_date, appt.start_time) and end_time > datetime.combine(appt.appt_date, appt.end_time):
                    raise ValidationError(
                        "unavailable time slot")
                if start_time < datetime.combine(appt.appt_date, appt.end_time) and end_time > datetime.combine(appt.appt_date, appt.end_time):
                    raise ValidationError(
                        "unavailable time slot")

        return super().validate(attrs)

    def create(self, validated_data):

        appointment = super().create(validated_data)

        appointment.save()

        return appointment


class BookingDetailsSerializer(serializers.ModelSerializer):
    service = serializers.ReadOnlyField(
        source='service_id.name')
    user = serializers.ReadOnlyField(source='user.username')
    recipients = serializers.IntegerField()
    start_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField(read_only=True)
    approved = serializers.BooleanField()
    appt_status = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    total_price = serializers.IntegerField()
    payment_method = serializers.CharField()
    location = ViewLocationSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "service", "user", "start_date", "start_time", "end_time", "approved", "recipients",
                  "appt_status", "created_at", "updated_at", "total_price", "payment_method", "location"]


class BookingUpdateStatusSerializer(serializers.ModelSerializer):
    appt_status = serializers.CharField()
    approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = Appointment
        fields = ["appt_status", "approved", ]


class BookingReschedule(serializers.ModelSerializer):
    start_date = serializers.DateField(required=True)
    start_time = serializers.TimeField(required=True)
    end_time = serializers.TimeField(required=True)

    class Meta:
        model = Appointment
        fields = ["start_date", "start_time", "end_time"]


class BookedSlotListSerializer(serializers.ModelSerializer):
    appt_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    class Meta:
        model = BookedSlot
        fields = ["id", "appointment", "appt_date", "start_time", "end_time"]


class BookedDateView(serializers.ModelSerializer):
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    class Meta:
        model = BookedSlot
        fields = ["start_time", "end_time"]


class LocationSerializer(serializers.ModelSerializer):
    street = serializers.CharField(required=True)
    surburb = serializers.CharField()
    city = serializers.CharField(required=True)
    zip_code = serializers.CharField(required=True)

    class Meta:
        model = AppLocation
        fields = ['street', 'city', 'surburb', 'zip_code']


class LocationViewSerializer(serializers.ModelSerializer):
    street = serializers.CharField()
    surburb = serializers.CharField()
    city = serializers.CharField()
    zip_code = serializers.CharField()

    class Meta:
        model = AppLocation
        fields = ['street', 'city', 'surburb', 'zip_code']
