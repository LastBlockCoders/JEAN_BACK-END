from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [path("create/", views.CreateServicesView.as_view(), name="create"),
               path("detail/<int:service_id>/",
                    views.ServiceDetailsView.as_view(), name="service-details"),
               path("all/", views.ServiceListView.as_view(), name="all-services"),
               path("update/<int:service_id>/", views.ServiceDetailsUpdateView.as_view(), name="service-update"), ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
