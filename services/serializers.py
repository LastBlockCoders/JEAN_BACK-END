from asyncore import read
from datetime import datetime, timedelta
from unicodedata import category
from rest_framework import serializers
from .models import Service, Service_Category
from rest_framework.validators import ValidationError
from django.utils.translation import gettext_lazy as _


class CreateServiceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    category_id = serializers.CharField(required=True)
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
        max_recipients = attrs["max_recipients"]

        if not name:
            raise ValidationError('please provide service name')
        if not description:
            raise ValidationError('please provide service description')
        if not duration:
            raise ValidationError('please provide service duration')
        if not price:
            raise ValidationError('please provide service price')

        if not max_recipients:
            raise ValidationError(
                'please provide maximum number of recipients')

        if price < 50:
            raise ValidationError('service price is less than R50')

        if max_recipients > 10:
            raise ValidationError(
                'only maximum of 10 recipients is currently allowed')

        return super().validate(attrs)

    def create(self, validated_data):

        service = super().create(validated_data)

        service.save()

        return service


class ViewServicesSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    type = serializers.CharField()
    description = serializers.CharField()
    category = serializers.ReadOnlyField(source='category.name')
    location_requirements = serializers.CharField()
    image1 = serializers.ImageField(use_url=True)
    image2 = serializers.ImageField(use_url=True)
    image3 = serializers.ImageField(use_url=True)
    duration = serializers.DurationField()
    promo_price = serializers.IntegerField()
    featured = serializers.IntegerField()
    price = serializers.IntegerField()
    max_recipients = serializers.IntegerField()
    payment_options = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'type', 'category', 'description', 'location_requirements', 'promo_price', 'featured',
                  'image1', 'image2', 'image3', 'duration', 'price', 'max_recipients', 'payment_options', 'status']


class ServicesPriceUpdateSerializers(serializers.ModelSerializer):
    price = serializers.IntegerField(required=True)
    image1 = serializers.ImageField(required=False)
    image2 = serializers.ImageField(required=False)
    image3 = serializers.ImageField(required=False)
    status = serializers.CharField(required=True)

    class Meta:
        model = Service
        fields = ['price', 'status',
                  'image1', 'image2', 'image3']


class CategoryListViewSerializers(serializers.ModelSerializer):
    name = serializers.CharField()
    image = serializers.ImageField(use_url=True)
    description = serializers.CharField()

    class Meta:
        model = Service_Category
        fields = ["id", "name", "image", "description"]

    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)


class CategoryCreate(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    image = serializers.ImageField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Service_Category
        fields = ["name", "description", "image"]


class ReceiveServiceID(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Service
        fields = ["name"]

    name = serializers.CharField()

    class Meta:
        model = Service_Category
        fields = ["name"]
