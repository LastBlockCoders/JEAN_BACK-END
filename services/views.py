
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from .models import Service, Service_Category
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

            response = {
                "message": "Service added successfully.",
                "data": deserializer.data,
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
    serializer_class = serializers.ViewServicesSerializer
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
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request: Request):
        services = get_list_or_404(Service.objects.all())

        serializer = self.serializer_class(instance=services, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CategoryListView(generics.GenericAPIView):
    serializer_class = serializers.CategoryListViewSerializers
    permission_classes = []

    def get(self, request: Request):
        category = get_list_or_404(Service_Category.objects.all())

        serializer = self.serializer_class(instance=category, many=True)

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
