from django.urls import path
from . import views

urlpatterns = [
    path("latest/", views.GetLatestJoinedUser.as_view(), name="new-users"),
    path("monthly/", views.UsersMonthly.as_view(), name='monthly-users')]
