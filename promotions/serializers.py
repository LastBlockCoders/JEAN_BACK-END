from rest_framework import serializers
from datetime import datetime
from .models import Coupon
from rest_framework.validators import ValidationError


class CouponCodeCreateSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    amount = serializers.IntegerField()
    once_off = serializers.BooleanField()
    is_used = serializers.BooleanField(read_only=True)
    created_at = serializers.DateField(read_only=True,
                                       default=serializers.CreateOnlyDefault(datetime.now()))
    expiry = serializers.DateField()

    class Meta:
        model = Coupon
        fields = ["code", "description", "amount",
                  "once_off", "is_used", "created_at"]

    def validate(self, attrs):
        code = attrs["code"]
        amount = attrs["amount"]

        if code.len() < 3:
            raise ValidationError("code must be more than 3 characters")

        if amount <= 0:
            raise ValidationError("amount must be more than R0")

        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)


class CouponCodeDetailSerializer(serializers.Serializer):
    code = serializers.CharField()
    description = serializers.CharField()
    amount = serializers.IntegerField()
    once_off = serializers.BooleanField()
    is_used = serializers.BooleanField()
    expiry = serializers.DateField()

    class Meta:
        model = Coupon
        fields = ["id", "code", "description", "amount",
                  "once_off", "is_used", ]


class CouponCodeApplySerializer(serializers.Serializer):
    is_used = serializers.BooleanField()

    class Meta:
        model = Coupon
        fields = ["is_used"]
