from django.urls import path
from . import views

urlpatterns = [path("request/", views.BookingRequestCreateView.as_view(), name="request"),
               path("list/", views.BookingRequestListView.as_view(), name="list"),
               path("view/<int:appointment_id>/",
                    views.BookingRequestDetailView.as_view(), name="view"),
               path("update-reply/<int:appointment_id>/",
                    views.BookingRequestReplyView.as_view(), name="reply"),
               path("cancel/<int:appointment_id>/",
                    views.BookingRequestCancelView.as_view(), name="cancel"),
               path("reschedule/<int:appointment_id>/",
                    views.UserRescheduleView.as_view(), name="reschedule"),
               path("account/<int:user_id>/bookings/",
                    views.UserBookingRequestsView.as_view(), name="account-bookings"),
               path("account/<int:user_id>/bookings/<int:appointment_id>/",
                    views.UserBookingRequestDetailView.as_view(), name="account-detail-booking"),
               path("booked-slots/", views.BookedSlotsListView.as_view(),
                    name="booked-slots"),
               path("location/", views.AppLocationCreateView.as_view(),
                    name="location"),
               path("cart/<int:service_id>/", views.CartRequestsStore.as_view(), name="cart-item")]
