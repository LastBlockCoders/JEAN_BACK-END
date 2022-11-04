from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [path("create/", views.CreateServicesView.as_view(), name="create"),
               path("delete/<int:service_id>/",
                    views.DeleteServiceView.as_view(), name='delete'),
               path("detail/<int:service_id>/",
                    views.ServiceDetailsView.as_view(), name="service-details"),
               path("per-request/<int:service_id>/", views.ServiceRequestPerMonth.as_view(),
                    name='requets-per-month'),

               path("all/", views.ServiceListView.as_view(), name="all-services"),
               path("update/<int:service_id>/",
                    views.ServiceDetailsUpdateView.as_view(), name="service-update"),
               path("featured/", views.FeatureService.as_view(), name="featured"),
               path("random/", views.Feature4service.as_view(), name="random-4"),
               path("category/", views.CategoryListView.as_view(), name="category"),
               path("category/create/", views.CreateCategoryView.as_view(), name="create-category")] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
