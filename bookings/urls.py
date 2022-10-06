from django.urls import path
from . import views

urlpatterns = [path("request/", views.BookingRequestCreateView.as_view(), name="request"),
               path("list/", views.BookingRequestListView.as_view(), name="list"),
               path("view/<int:appointment_id>/",
                    views.BookingRequestDetailView.as_view(), name="view"),
               path("update-status/<int:appointment_id>/",
                    views.BookingRequestStatusUpdateView.as_view(), name="update-status"),
               path("account/<int:user_id>/bookings/",
                    views.UserBookingRequestView.as_view(), name="account-bookings"),
               path("booked-slots/", views.BookedSlotsListView.as_view(), name="booked-slots"), ]
