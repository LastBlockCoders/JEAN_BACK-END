from unittest.util import _MAX_LENGTH
from .models import User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.validators import ValidationError


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=50)
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)
    password = serializers.CharField(min_length=8, write_only=True)
    date_of_birth = serializers.DateField()
    gender = serializers.CharField(max_length=6)

    class Meta:
        model = User
        fields = ["email", "username", "phone_number",
                  "password", "date_of_birth", "gender"]

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        phonenumber_exists = User.objects.filter(
            phone_number=attrs['phone_number']).exists()

        if email_exists:
            raise ValidationError("Email already in use")

        if phonenumber_exists:
            raise ValidationError("Phone number already in use")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()

        return user
