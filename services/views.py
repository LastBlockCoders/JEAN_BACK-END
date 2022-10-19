
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from .models import Service
from services import serializers

# Create your views here.


class CreateServicesView(generics.GenericAPIView):
    serializer_class = serializers.CreateServiceSerializer
    permission_classes = [IsAdminUser]

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

        return Response(data=deserializer.errors, status=status.HTTP_200_OK)


class ServiceDetailsView(generics.GenericAPIView):
    serializer_class = serializers.ViewServicesSerializer

    def get(self, request: Request, service_id):
        data = request.data
        service = get_object_or_404(Service, pk=service_id)

        serializer = self.get_serializer_class(instance=service)

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceDetailsUpdateView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.CreateServiceSerializer

    def put(self, request: Request, service_id):
        data = request.data
        service = get_object_or_404(Service, pk=service_id)

        serializer = self.get_serializer_class(instance=service)

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceListView(generics.GenericAPIView):
    serializer_class = serializers.ViewServicesSerializer

    def get(self, request: Request):
        services = get_list_or_404(Service.objects.all())

        serializer = self.serializer_class(instance=services, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
