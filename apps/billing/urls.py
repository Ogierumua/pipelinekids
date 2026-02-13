from django.urls import path
from . import views

urlpatterns = [
    path("pricing/", views.pricing, name="billing_pricing"),
    path("checkout/", views.create_checkout_session, name="billing_checkout"),
    path("success/", views.billing_success, name="billing_success"),
    path("cancel/", views.billing_cancel, name="billing_cancel"),
]
