from rest_framework import serializers
from .models import Service


class CreateServiceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField()
    location_requirements = serializers.CharField()
    image1 = serializers.ImageField(required=True)
    image2 = serializers.ImageField()
    image3 = serializers.ImageField()
    duration = serializers.DurationField(required=True)
    price = serializers.IntegerField(required=True)
    max_recipients = serializers.IntegerField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'location_requirements', 'image1',
                  'image2', 'image3', 'duration', 'price', 'max_recipients']


class ViewServicesSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    location_requirements = serializers.CharField()
    image1 = serializers.ImageField()
    image2 = serializers.ImageField()
    image3 = serializers.ImageField()
    duration = serializers.DurationField()
    price = serializers.IntegerField()
    max_recipients = serializers.IntegerField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'location_requirements',
                  'image1', 'image2', 'image3', 'duration', 'price', 'max_recipients']


class ServicesPriceUpdateSerializers(serializers.ModelSerializer):
    price = serializers.IntegerField()

    class Meta:
        model = Service
        fields = ['price']
