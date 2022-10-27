from rest_framework.fields import CurrentUserDefault
from urllib import request
import pytz
from datetime import datetime, timedelta
from email.policy import default
from rest_framework import serializers
from .models import Appointment, BookedSlot, AppLocation, Booking
from services.models import Service
from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError

User = get_user_model()


class CartBookingStore(serializers.ModelSerializer):
    recipients = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)

    class Meta:
        model = Booking
        fields = ["id", "recipients", "amount"]

    def validate(self, attrs):

        recipients = attrs["recipients"]

        if recipients > 10:
            raise ValidationError("recipients exceeds 10 people")

        return super().validate(attrs)

    def create(self, validated_data):

        cart = super().create(validated_data)

        cart.save()

        return cart


class DisplayBooking(serializers.ModelSerializer):
    service_id = serializers.ReadOnlyField(source='service_id.name')
    recipients = serializers.IntegerField(required=True)
    amount = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = ["id", "service_id", "recipients", "amount"]


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
    )
    booking = DisplayBooking(many=True, read_only=True)
    start_date = serializers.DateField(required=True)
    start_time = serializers.TimeField(required=True)
    end_time = serializers.TimeField(required=True)
    appt_status = serializers.HiddenField(default='pending')
    approved = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True,
                                           default=serializers.CreateOnlyDefault(datetime.now()))
    updated_at = serializers.DateTimeField(
        read_only=True, default=datetime.now())
    paid = serializers.BooleanField(read_only=True)
    total_price = serializers.IntegerField(),
    payment_status = serializers.CharField(read_only=True, default='UNPAID')
    payment_method = serializers.CharField(default='EFT/Card')

    class Meta:
        model = Appointment
        fields = ["booking", "user", "start_date", "start_time", "end_time",
                  "appt_status", "approved", "created_at", "updated_at", "paid", "total_price", "payment_status", "payment_method"]

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
        end_time = end_time + timedelta(minutes=30)
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
    booking = DisplayBooking(many=True, read_only=True)
    start_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    approved = serializers.BooleanField()
    appt_status = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    paid = serializers.BooleanField()
    total_price = serializers.IntegerField()
    payment_status = serializers.CharField()
    payment_method = serializers.CharField()

    class Meta:
        model = Appointment
        fields = ["id", "booking", "start_date", "start_time", "end_time", "approved",
                  "appt_status", "created_at", "updated_at", "paid", "total_price", "payment_status", "payment_method"]


class BookingUpdateStatusSerializer(serializers.ModelSerializer):
    appt_status = serializers.CharField()
    approved = serializers.BooleanField(read_only=True)
    payment_status = serializers.CharField(read_only=True)
    payment_method = serializers.CharField(read_only=True)
    paid = serializers.BooleanField(read_only=True)

    class Meta:
        model = Appointment
        fields = ["appt_status", "approved", "payment_method", "paid", ]


class BookedSlotListSerializer(serializers.ModelSerializer):
    appt_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    class Meta:
        model = BookedSlot
        fields = ["id", "appointment", "appt_date", "start_time", "end_time"]


class LocationSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    country = serializers.CharField(required=True)
    zip_code = serializers.CharField(required=True)

    class Meta:
        model = AppLocation
        fields = ['address', 'city', 'country', 'zip_code']

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user
