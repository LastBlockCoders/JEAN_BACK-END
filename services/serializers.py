from datetime import datetime, timedelta
from pydoc import describe
from rest_framework import serializers
from .models import Service
from rest_framework.validators import ValidationError


class CreateServiceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=True)
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

    def validate(self, attrs):
        name = attrs["name"]
        description = attrs["description"]
        duration = attrs["duration"]
        price = attrs["price"]

        if not name:
            raise ValidationError('please provide service name')
        if not description:
            raise ValidationError('please provide service description')
        if not duration:
            raise ValidationError('please provide service duration')
        if not price:
            raise ValidationError('please provide service price')

        if price < 50:
            raise ValidationError('service price is less than R50')

        return super().validate(attrs)

    def create(self, validated_data):

        service = super().create(validated_data)

        service.save()

        return service


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
