
from django.contrib import admin
from django.urls import path, include
from accounts.views import ActivateUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path("clients/", include("accounts.urls")),
    path('appointment/', include("bookings.urls")
         ), path("auth/", include("djoser.urls")), path('auth/', include('djoser.urls.jwt')), path("services/", include('services.urls')),
    path(
        "accounts/activate/<uid>/<token>",
        ActivateUser.as_view({"get": "activation"}),
        name="activation",
    ),
    path("promotions/", include('promotions.urls'),)
]
