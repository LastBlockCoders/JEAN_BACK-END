
from datetime import datetime
from tracemalloc import start
from drf_multiple_model.views import ObjectMultipleModelAPIView
from django.shortcuts import render, get_object_or_404
from .models import Appointment, BookedSlot
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from bookings import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


class BookingRequestCreateView(generics.GenericAPIView):
    serializer_class = serializers.BookingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        data = request.data
        user = request.user
        deserializedData = self.serializer_class(data=data)

        if deserializedData.is_valid():
            deserializedData.save(user=user)

            response = {
                "message": "booking request successfully submitted",
                "data": deserializedData.data,
            }

            return Response(data=response, status=status.HTTP_202_ACCEPTED)

        return Response(data=deserializedData.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class BookingRequestListView(generics.GenericAPIView):
    serializer_class = serializers.BookingDetailsSerializer
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request):
        appointments = Appointment.objects.all()

        serializer = self.serializer_class(instance=appointments, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class BookingRequestDetailView(generics.GenericAPIView):
    serializer_class = serializers.BookingDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, appointment_id):

        appointment = get_object_or_404(Appointment, pk=appointment_id)

        serializer = self.serializer_class(instance=appointment)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, appointment_id):
        permission_classes = [IsAdminUser]
        data = request.data
        appointment = get_object_or_404(Appointment, pk=appointment_id)

        serializer = self.get_serializer_class(instance=appointment)

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingRequestStatusUpdateView(generics.GenericAPIView):
    serializer_class = serializers.BookingUpdateStatusSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, appointment_id):
        data = request.data
        appointment = get_object_or_404(
            Appointment, pk=appointment_id)
        sdate = appointment.start_date
        start_time = datetime.combine(sdate, appointment.start_time)
        end_time = datetime.combine(sdate, appointment.end_time)
        booked_appts = BookedSlot.objects.filter(appt_date=sdate)

        serializer = self.serializer_class(data=data, instance=appointment)

        if serializer.is_valid():
            if booked_appts.exists():
                if serializer.validated_data["appt_status"] == "schedule":
                    for appt in booked_appts:
                        if start_time > datetime.combine(appt.appt_date, appt.start_time) and end_time < datetime.combine(appt.appt_date, appt.end_time):
                            serializer.validated_data["appt_status"] = "rejected"
                            serializer.save()
                            response = {"message": "an appointment is already scheduled during this time",
                                        "data": serializer.data}
                            return Response(data=response, status=status.HTTP_200_OK)
                        elif start_time < datetime.combine(appt.appt_date, appt.start_time) and end_time > datetime.combine(appt.appt_date, appt.end_time):
                            serializer.validated_data["appt_status"] = "rejected"
                            serializer.save()
                            response = {"message": "an appointment is already scheduled during this time",
                                        "data": serializer.data}
                            return Response(data=response, status=status.HTTP_200_OK)
                        elif start_time < datetime.combine(appt.appt_date, appt.end_time) and end_time > datetime.combine(appt.appt_date, appt.end_time):
                            serializer.validated_data["appt_status"] = "pending"
                            serializer.save()
                            response = {"message": "an appointment is already scheduled during this time",
                                        "data": serializer.data}
                            return Response(data=response, status=status.HTTP_200_OK)
                        elif start_time == datetime.combine(appt.appt_date, appt.start_time) and end_time == datetime.combine(appt.appt_date, appt.end_time):
                            serializer.validated_data["appt_status"] = "pending"
                            serializer.save()
                            response = {"message": "an appointment is already scheduled during this time",
                                        "data": serializer.data}
                            return Response(data=response, status=status.HTTP_200_OK)

                        serializer._validated_data["approved"] = True
                        serializer.save()
                        bookslot = BookedSlot(
                            appointment=appointment, start_time=start_time.time(), end_time=end_time.time(), appt_date=appointment.start_date)
                        bookslot.save()

                        return Response(data=serializer.data, status=status.HTTP_200_OK)

                elif serializer.validated_data["appt_status"] == "reject":
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_200_OK)

            if serializer.validated_data["appt_status"] == 'schedule':
                serializer._validated_data["approved"] = True
                serializer.save()
                bookslot = BookedSlot(
                    appointment=appointment, start_time=start_time.time(), end_time=end_time.time(), appt_date=appointment.start_date)
                bookslot.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            elif serializer.validated_data["appt_status"] == "reject":
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBookingRequestView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.BookingDetailsSerializer

    def get(self, request: Request, user_id):
        user = User.objects.get(pk=user_id)

        appointments = Appointment.objects.all().filter(user=user)
        serializer = self.serializer_class(instance=appointments, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserBookingRequestDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.BookingDetailsSerializer

    def get(self, request: Request, user_id, order_id):
        user = User.objects.get(pk=user_id)
        appointment = Appointment.objects.all().filter(user=user).get(pk=order_id)

        serializers = self.serializer_class(instance=appointment)

        return Response(data=serializers.data, status=status.HTTP_200_OK)


class BookedSlotsListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = serializers.BookedSlotListSerializer

    def get(self, request: Request):
        bookedslots = BookedSlot.objects.all()

        serializer = self.serializer_class(instance=bookedslots, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AppLocationCreateView(generics.GenericAPIView):
    serializer_class = serializers.AppLocation
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        data = request.data
        user = request.user
        deserializer = self.serializer_class(data=data)

        if deserializer.is_valid():
            deserializer.save(user=user)

            response = {
                "message": "location succeesfully saved",
                "data": deserializer.data,
            }

            return Response(data=response, status=status.HTTP_202_ACCEPTED)

        return Response(data=deserializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
