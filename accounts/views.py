from datetime import datetime
from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from accounts import serializers
from rest_framework.permissions import IsAdminUser
from accounts.models import User
import pytz

# Create your views here.


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())

        # this line is the only change from the base implementation.
        kwargs["data"] = {"uid": self.kwargs["uid"],
                          "token": self.kwargs["token"]}

        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetLatestJoinedUser(generics.GenericAPIView):
    serializer_class = serializers.UserDetails
    permission_classes = [IsAdminUser]

    def get(self, request: Request):
        this_month = datetime.today().month
        this_year = datetime.today().year
        tz = datetime.today()
        pytz.utc.localize(
            tz).tzinfo

        date = datetime(int(this_year), int(this_month), 1)

        queryset = User.objects.exclude(
            date_joined__gte=datetime.today()).filter(date_joined__gte=date)[:10]

        serializer = self.serializer_class(instance=queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UsersMonthly(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request):
        date = datetime.today().date()
        this_month = date.month
        this_year = date.year

        current_date = datetime(int(this_year), int(this_month), 1)

        pytz.utc.localize(
            current_date)

        this_months = User.objects.filter(
            date_joined__month=this_month)

        last_months = User.objects.exclude(date_joined__gte=current_date).filter(
            date_joined__month=this_month-1)

        current_month_users = len(this_months)
        last_month_users = len(last_months)

        dict = {"new": current_month_users, "old": last_month_users}

        return Response(data=dict, status=status.HTTP_200_OK)
