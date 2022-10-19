from django.urls import path
from . import views

urlpatterns = [path("create/", views.CreateCouponView.as_view(), name="create"),
               path("list/", views.GetCouponListView.as_view(), name='list'),
               path("view/", views.GetCouponDetailsView.as_view(), name='view'),
               path("apply/", views.ApplyCouponView.as_view(), name='apply'),
               path("my-coupons/<int:user_id>/", views.GetUserCouponView.as_view(), name='user-coupons')]
