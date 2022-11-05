import pytz
import operator as op
from datetime import datetime
from django.db.models import Count, DateField, Sum
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
import random

import services
from .models import Service, Service_Category
from bookings.models import Appointment
from services import serializers
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.


class CreateServicesView(generics.GenericAPIView):
    serializer_class = serializers.CreateServiceSerializer
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request: Request):
        data = request.data
        deserializer = self.serializer_class(data=data)

        if deserializer.is_valid():
            deserializer.save()
            serializer = self.serializer_class(
                instance=services)

            response = {
                "message": "Service added successfully.",
                "data": serializer.data,
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=deserializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class ServiceDetailsView(generics.GenericAPIView):
    serializer_class = serializers.ViewServicesSerializer
    permission_classes = []
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request: Request, service_id):

        service = get_object_or_404(Service, pk=service_id)

        serializer = self.serializer_class(instance=service)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ServiceDetailsUpdateView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.ServicesPriceUpdateSerializers
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request: Request, service_id):
        data = request.data
        service = get_object_or_404(Service, pk=service_id)

        serializer = self.serializer_class(instance=service, data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class ServiceListView(generics.GenericAPIView):
    serializer_class = serializers.ViewServicesSerializer
    permission_classes = []
    queryset = Service.objects.all()

    def get(self, request: Request):
        services = get_list_or_404(Service.objects.all())
        queryset = Service.objects.all()
        services = queryset

        serializer = self.serializer_class(instance=services, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CategoryListView(generics.GenericAPIView):
    serializer_class = serializers.CategoryListViewSerializers
    permission_classes = []

    def get(self, request: Request):
        category = get_list_or_404(Service_Category.objects.all())

        serializer = self.serializer_class(instance=category, context={"request":
                                                                       request}, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreateCategoryView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.CategoryCreate

    def post(self, request: Request):

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():

            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class DeleteServiceView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def delete(self, request: Request, service_id):

        service = get_object_or_404(Service, pk=service_id)

        service.delete()

        return Response(status=status.HTTP_200_OK)


class ServiceRequestPerMonth(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, service_id):
        service = Service.objects.get(pk=service_id)
        date = datetime.today().date()
        year = date.year
        this_month = date.month
        last_month = this_month - 1

        date = datetime(int(year), int(this_month), 1)
        pytz.utc.localize(
            date)
        last_month_date = datetime(int(year), int(last_month), 1)
        pytz.utc.localize(
            last_month_date)

        appts_this_month = Appointment.objects.exclude(
            created_at__gte=datetime.today()).filter(
            created_at__gte=date).values_list('booking', flat=True)
        this_month = appts_this_month

        appts_last_month = Appointment.objects.exclude(
            created_at__gte=date).filter(
            created_at__gte=last_month_date).values_list('booking', flat=True)
        last_month = appts_last_month

        if this_month.exists() and last_month.exists():
            new = op.countOf(this_month, service_id)
            last = op.countOf(last_month, service_id)

            dict = [{"id": int(date.month), "total": new}, {
                "id": int(last_month_date.month), "total": last}]

            return Response(data=dict, status=status.HTTP_200_OK)

        if not this_month and last_month.exists():
            new = 0
            last = op.countOf(last_month, service_id)

            dict = [{"id": int(date.month), "total": new}, {
                "id": int(last_month_date.month), "total": last}]

            return Response(data=dict, status=status.HTTP_200_OK)

        if not last_month and this_month.exists():
            new = op.countOf(this_month, service_id)
            last = 0

            dict = [{"id": int(date.month), "total": new}, {
                "id": int(last_month_date.month), "total": last}]

            return Response(data=dict, status=status.HTTP_200_OK)


class FeatureService(generics.GenericAPIView):
    serializer_class = serializers.ViewServicesSerializer
    permission_classes = []

    def get(self, request: Request):

        queryset = list(Service.objects.filter(featured=1))

        services = random.sample(queryset, 3)

        serializer = self.serializer_class(instance=services, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Feature4service(generics.GenericAPIView):
    serializer_class = serializers.ViewServicesSerializer
    permission_classes = []

    def get(self, request: Request):

        queryset = list(Service.objects.all())

        services = random.sample(queryset, 4)

        serializer = self.serializer_class(instance=services, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SearchList(generics.GenericAPIView):
    queryset = Service.objects.all()
    serializer_class = serializers.ViewServicesSerializer
    name = 'serviceList'
    filter_fields = (
        'name',
        'description',
    )


class GetByCategory(generics.GenericAPIView):
    serializer_class = serializers.ViewServicesSerializer
    permission_classes = []

    def get(self, request: Request, category_id):

        cat = Service_Category.objects.get(pk=category_id)

        queryset = list(Service.objects.all().filter(category=cat))

        serializer = self.serializer_class(instance=queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
