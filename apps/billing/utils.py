from django.urls import path
from . import views
from .webhooks import stripe_webhook
from functools import wraps

urlpatterns = [
    path("subscribe/", views.subscribe, name="subscribe"),
    path("checkout/", views.create_checkout, name="create_checkout"),
    path("success/", views.success, name="billing_success"),
    path("cancel/", views.cancel, name="billing_cancel"),
    path("webhook/", stripe_webhook, name="stripe_webhook"),
]



def subscription_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        # TEMP: allow everyone through for now
        return view_func(request, *args, **kwargs)
    return _wrapped
