from asyncore import read
from datetime import datetime, timedelta
from unicodedata import category
from rest_framework import serializers
from .models import Service, Service_Category
from rest_framework.validators import ValidationError


class CreateServiceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    category_id = serializers.CharField()
    type = serializers.CharField()
    description = serializers.CharField(required=True)
    location_requirements = serializers.CharField()
    image1 = serializers.ImageField(required=False)
    image2 = serializers.ImageField(required=False)
    image3 = serializers.ImageField(required=False)
    duration = serializers.DurationField(required=True)
    price = serializers.IntegerField(required=True)
    max_recipients = serializers.IntegerField()
    payment_options = serializers.CharField()
    status = serializers.CharField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'category_id', 'type', 'description', 'location_requirements', 'image1',
                  'image2', 'image3', 'duration', 'price', 'max_recipients', 'payment_options', 'status']

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
    type = serializers.CharField()
    description = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    location_requirements = serializers.CharField()
    image1 = serializers.ImageField()
    image2 = serializers.ImageField()
    image3 = serializers.ImageField()
    duration = serializers.DurationField()
    price = serializers.IntegerField()
    max_recipients = serializers.IntegerField()
    payment_options = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'type', 'category', 'description', 'location_requirements',
                  'image1', 'image2', 'image3', 'duration', 'price', 'max_recipients', 'payment_options', 'status']


class ServicesPriceUpdateSerializers(serializers.ModelSerializer):
    price = serializers.IntegerField()

    class Meta:
        model = Service
        fields = ['price']


class CategoryListViewSerializers(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Service_Category
        fields = ["name", "description"]


class ReceiveServiceID(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Service
        fields = ["name"]
