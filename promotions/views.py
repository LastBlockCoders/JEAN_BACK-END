from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import generics
from promotions import serializers
from .models import Coupon
# Create your views here.


class CreateCouponView(generics.GenericAPIView):
    serializer_class = serializers.CouponCodeCreateSerializer
    permission_classes = [IsAdminUser]

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "Service added successfully.",
                "data": serializer.data,
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCouponListView(generics.GenericAPIView):
    serializer_class = serializers.CouponCodeDetailSerializer
    permission_classes = [IsAdminUser]

    def get(self, request: Request):
        coupons = get_list_or_404(Coupon.objects.all())

        serializer = self.serializer_class(instance=coupons, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetCouponDetailsView(generics.GenericAPIView):
    serializer_class = serializers.CouponCodeDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request, coupon_id):
        data = request.data
        coupon = get_object_or_404(Coupon, pk=coupon_id)

        serializer = self.get_serializer_class(instance=coupon)

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplyCouponView(generics.GenericAPIView):
    serializer_class = serializers.CouponCodeApplySerializer

    def put(self, request, coupon_id):
        data = request.data
        coupon = get_object_or_404(Coupon, pk=coupon_id)

        serializer = self.serializer_class(data=data, instance=coupon)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserCouponView(generics.GenericAPIView):
    serializer_class = serializers.CouponCodeDetailSerializer

    def get(self, request: Request, user_id):
        coupons = Coupon.objects.all().filter(user_id=user_id)

        serializers = self.serializer_class(instance=coupons, many=True)

        return Response(data=serializers.data, status=status.HTTP_200_OK)
