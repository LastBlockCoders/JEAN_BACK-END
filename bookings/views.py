
from services.models import Service
from datetime import datetime
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Appointment, BookedSlot, AppLocation
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from bookings import serializers
from django.contrib.auth import get_user_model
from .function import attempt_json_deserialize
User = get_user_model()
# Create your views here.


class CartRequestsStore(generics.GenericAPIView):
    serializer_class = serializers.CartBookingStore
    permission_classes = []
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request: Request, service_id):
        data = request.data
        service = get_object_or_404(Service, pk=service_id)
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.validated_data["service_id"] = service
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class BookingRequestCreateView(generics.GenericAPIView):
    serializer_class = serializers.BookingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        data = request.data
        user = request.user

        location = AppLocation.objects.get(user=user)

        booking_data = data.get("booking")

        booking_data = attempt_json_deserialize(
            booking_data, expect_type=list)

        deserializedData = self.serializer_class(data=data)

        if deserializedData.is_valid():
            deserializedData._validated_data["booking"] = booking_data
            deserializedData._validated_data["user"] = user
            deserializedData._validated_data["location"] = location
            deserializedData.save(user=user)

            return Response(data=deserializedData.data, status=status.HTTP_202_ACCEPTED)

        return Response(data=deserializedData.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class BookingRequestListView(generics.GenericAPIView):
    serializer_class = serializers.BookingDetailsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request):
        appointments = Appointment.objects.all()

        serializer = self.serializer_class(instance=appointments, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class BookingRequestDetailView(generics.GenericAPIView):
    serializer_class = serializers.BookingDetailsSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, appointment_id):

        appointment = get_object_or_404(Appointment, pk=appointment_id)

        serializer = self.serializer_class(instance=appointment)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, appointment_id):
        data = request.data
        appointment = get_object_or_404(Appointment, pk=appointment_id)

        serializer = self.get_serializer_class(instance=appointment)

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingRequestReplyView(generics.GenericAPIView):
    serializer_class = serializers.BookingUpdateStatusSerializer
    permission_classes = [IsAdminUser]

    def put(self, request: Request, appointment_id):
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
                if serializer.validated_data["appt_status"] == "accept":
                    for appt in booked_appts:
                        if start_time > datetime.combine(appt.appt_date, appt.start_time) and end_time < datetime.combine(appt.appt_date, appt.end_time):
                            serializer.validated_data["appt_status"] = "rejected"
                            serializer.save()
                            response = {"message": "an appointment is already scheduled for this time",
                                        "data": serializer.data}
                            return Response(data=response, status=status.HTTP_200_OK)
                        elif start_time < datetime.combine(appt.appt_date, appt.start_time) and end_time > datetime.combine(appt.appt_date, appt.end_time):
                            serializer.validated_data["appt_status"] = "rejected"
                            serializer.save()
                            response = {"message": "an appointment is already scheduled for this time",
                                        "data": serializer.data}
                            return Response(data=response, status=status.HTTP_200_OK)
                        elif start_time < datetime.combine(appt.appt_date, appt.end_time) and end_time > datetime.combine(appt.appt_date, appt.end_time):
                            serializer.validated_data["appt_status"] = "rejected"
                            serializer.save()
                            response = {"message": "an appointment is already scheduled during this time",
                                        "data": serializer.data}
                            return Response(data=response, status=status.HTTP_200_OK)
                        elif start_time == datetime.combine(appt.appt_date, appt.start_time) and end_time == datetime.combine(appt.appt_date, appt.end_time):
                            serializer.validated_data["appt_status"] = "rejected"
                            serializer.save()
                            response = {"message": "an appointment is already scheduled during this time",
                                        "data": serializer.data}
                            return Response(data=response, status=status.HTTP_200_OK)

                        serializer._validated_data["approved"] = True

                        if appointment.payment_method == "Cash":
                            serializer._validated_data["paid"] = True
                            serializer._validated_data["payment_status"] = "PAID"
                            serializer.save()
                            bookslot = BookedSlot(
                                appointment=appointment, start_time=start_time.time(), end_time=end_time.time(), appt_date=appointment.start_date)
                            bookslot.save()
                            return Response(data=serializer.data, status=status.HTTP_200_OK)

                        serializer.save()
                        bookslot = BookedSlot(
                            appointment=appointment, start_time=start_time.time(), end_time=end_time.time(), appt_date=appointment.start_date)
                        bookslot.save()

                        return Response(data=serializer.data, status=status.HTTP_200_OK)

                elif serializer.validated_data["appt_status"] == "reject":
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_200_OK)

            if serializer.validated_data["appt_status"] == 'accept':
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


class BookingRequestCancelView(generics.GenericAPIView):
    serializer_class = serializers.BookingUpdateStatusSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request: Request, appointment_id):
        data = request.data
        appointment = get_object_or_404(
            Appointment, pk=appointment_id)

        booked_slot = BookedSlot.objects.get(appointment=appointment)

        serializer = self.serializer_class(data=data, instance=appointment)

        if serializer.is_valid():
            booked_slot.delete()
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBookingRequestsView(generics.GenericAPIView):
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

    def get(self, request: Request, user_id, appointment_id):
        user = User.objects.get(pk=user_id)
        appointment = Appointment.objects.all().filter(user=user).get(pk=appointment_id)

        serializer = self.serializer_class(instance=appointment)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserRescheduleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.BookingReschedule

    def put(self, request: Request, appointment_id):
        data = request.data
        user = request.user
        appointment = Appointment.objects.all().filter(user=user).get(pk=appointment_id)

        serializer = self.serializer_class(data=data, instance=appointment)

        if serializer.is_valid():

            new_date = serializer.validated_data["start_date"]
            new_start = serializer.validated_data["start_time"]
            new_start = datetime.combine(new_date, new_start)
            new_end = serializer.validated_data["end_time"]
            new_end = datetime.combine(new_date, new_end)

            booked_appts = BookedSlot.objects.filter(appt_date=new_date)
            if booked_appts.exists():
                for appt in booked_appts:
                    if new_start > datetime.combine(appt.appt_date, appt.start_time) and new_end < datetime.combine(appt.appt_date, appt.end_time):
                        response = {"message": "an appointment is already scheduled for this time",
                                    "data": serializer.data}
                        return Response(data=response, status=status.HTTP_200_OK)
                    elif new_start < datetime.combine(appt.appt_date, appt.start_time) and new_end > datetime.combine(appt.appt_date, appt.end_time):
                        response = {"message": "an appointment is already scheduled for this time",
                                    "data": serializer.data}
                        return Response(data=response, status=status.HTTP_200_OK)
                    elif new_start < datetime.combine(appt.appt_date, appt.end_time) and new_end > datetime.combine(appt.appt_date, appt.end_time):
                        response = {"message": "an appointment is already scheduled during this time",
                                    "data": serializer.data}
                        return Response(data=response, status=status.HTTP_200_OK)
                    elif new_start == datetime.combine(appt.appt_date, appt.start_time) and new_end == datetime.combine(appt.appt_date, appt.end_time):
                        response = {"message": "an appointment is already scheduled during this time",
                                    "data": serializer.data}
                        return Response(data=response, status=status.HTTP_200_OK)

            booked_slot = BookedSlot.objects.get(appointment=appointment)
            booked_slot.appt_date = new_date
            booked_slot.start_time = new_start.time()
            booked_slot.end_time = new_end.time()
            booked_slot.save()

            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookedSlotsListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = serializers.BookedDateView

    def get(self, request: Request):
        data = request.data
        start_date = data["date"]
        bookedslots = BookedSlot.objects.all().filter(appt_date=start_date)

        serializer = self.serializer_class(instance=bookedslots, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AppLocationCreateView(generics.GenericAPIView):
    serializer_class = serializers.LocationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        data = request.data
        user = request.user
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.validated_data["user"] = user
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
