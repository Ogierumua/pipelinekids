import stripe
from functools import wraps
from django.conf import settings
from django.shortcuts import redirect
from .models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_or_create_subscription(user):
    sub, _ = Subscription.objects.get_or_create(parent=user)

    if not sub.stripe_customer_id:
        customer = stripe.Customer.create(
            email=getattr(user, "email", "") or None,
            name=getattr(user, "username", "") or None,
        )
        sub.stripe_customer_id = customer["id"]
        sub.save(update_fields=["stripe_customer_id"])

    return sub


def has_active_subscription(user) -> bool:
    if not user or not user.is_authenticated:
        return False

    try:
        sub = Subscription.objects.get(parent=user)
        return sub.status == "active"
    except Subscription.DoesNotExist:
        return False


def subscription_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if has_active_subscription(request.user):
            return view_func(request, *args, **kwargs)
        return redirect("billing_pricing")
    return _wrapped
